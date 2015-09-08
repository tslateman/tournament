#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import contextlib


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        conn = psycopg2.connect("dbname=tournament")
        return conn
    except:
        print("Database Connection Error")


@contextlib.contextmanager
def myCursor():
    """Function to consolidate db transaction code."""
    conn = connect()
    cursor = conn.cursor()
    try:
        yield cursor
    except:
        print("Database Cursor Error") 
    else:
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def deleteMatches():
    """Remove all the match records from the database."""
    with myCursor() as cursor:
        cursor.execute("TRUNCATE matches;")


def deletePlayers():
    """Remove all the player records from the database."""
    with myCursor() as cursor:
        cursor.execute("DELETE FROM players;")


def countPlayers():
    """Returns the number of players currently registered."""
    with myCursor() as cursor:
        cursor.execute("SELECT count(p.id) FROM players p \
            WHERE p.id != '-404';")
        result = cursor.fetchone()
    count = result[0]
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    with myCursor() as cursor:
        query = "INSERT INTO players (name) VALUES (%s);"
        parameter = (name,)
        cursor.execute(query, parameter)


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    with myCursor() as cursor:
        cursor.execute("SELECT id, name, wins, mcount FROM standings ")
        standings = cursor.fetchall()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    with myCursor() as cursor:
        query = "INSERT INTO matches (winner_id, loser_id) values (%s, %s);"
        parameters = (winner, loser)
        cursor.execute(query, parameters)


def reportBye(bye_player):
    """Registers a bye for a given player. Bye id assigned as '-404'.
    Updates both players table and matches table.

    Args:
      bye_player: player id receiving a bye.

    """

    with myCursor() as cursor:
        query = "INSERT INTO players (id, name) VALUES ('-404','bye');"
        cursor.execute(query)    
        query = "INSERT INTO matches (winner_id, loser_id) \
                values ('%s', '-404');"
        parameter = (bye_player,)
        cursor.execute(query, parameter)


def hasByes(player_id):
    """Checks if a player has byes checking the DB for bye ids '-404'

    Args:
      player_id: player id of player in question

    Returns: count of byes of player
    """

    with myCursor() as cursor:
        query = "SELECT count(id) FROM matches WHERE winner_id = %s \
                        and loser_id ='-404';"
        parameter = (player_id,)
        byecount = cursor.execute(query, parameter)
    return byecount


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    In cases where a bye is needed, bye is assigned id:'-404' name:'bye'

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    standings = playerStandings()
    players = [(row[0], row[1]) for row in standings]
    pairings = []

    # Bye condition for odd numbers of players
    if len(players) % 2 != 0:
        bye_index = len(players) - 1
        bye_player = players.pop()
        # Identify player without byes to assign a bye to
        while (hasByes(bye_player[0]) > 0 and bye_index > 0):
            players.insert(bye_index, byePlayer)
            bye_index -= 1
            bye_player = players.pop(bye_index)
        pairings.insert(
            bye_index, (bye_player[0], bye_player[1], '-404', 'bye'))

    # Assign players pairings
    while (len(players) > 1):
        player1 = players.pop()
        player2 = players.pop()
        pairings.insert(0, (player1[0], player1[1], player2[0], player2[1]))

    return pairings
