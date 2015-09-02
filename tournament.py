#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect(dbname="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("Database Connection Error")


def deleteMatches():
    """Remove all the match records from the database."""
    db, cursor = connect()
    cursor.execute("DELETE FROM matches;")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, cursor = connect()
    cursor.execute("DELETE FROM players;")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, cursor = connect()
    cursor.execute("SELECT count(p.id) FROM players p WHERE p.id != '-404';")
    result = cursor.fetchone()
    count = result[0]
    db.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    db, cursor = connect()
    query = "INSERT INTO players (name) VALUES (%s);"
    parameter = (name,)
    cursor.execute(query, parameter)
    db.commit()
    db.close()

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

    db, cursor = connect()
    cursor.execute("SELECT id, name, wins, mcount FROM standings ")
    standings = cursor.fetchall()
    db.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, cursor = connect()
    query = "INSERT INTO matches (winner_id, loser_id) values (%s, %s);"
    parameters = (winner, loser)
    cursor.execute(query, parameters)
    db.commit()
    db.close()


def reportBye(bye_player):
    """Registers a bye for a given player. Bye id assigned as '-404'.

    Args:
      bye_player: player id receiving a bye.

    """

    db, cursor = connect() 
    query = "INSERT INTO players (id, name) VALUES ('-404','bye');"
    cursor.execute(query)
    
    query = "INSERT INTO matches (winner_id, loser_id) values ('%s', '-404');"
    parameter = (bye_player,)
    cursor.execute(query, parameter)
    db.commit()
    db.close()


def hasByes(player_id):
    """Checks if a player has byes checking the DB for bye ids '-404'

    Args:
      player_id: player id of player in question

    Returns: count of byes of player
    """

    db, cursor = connect()
    query = "SELECT count(id) FROM matches WHERE winner_id = %s \
                        and loser_id ='-404';"
    parameter = (player_id,)
    byecount = cursor.execute(query, parameter)
    db.close()
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
        while (hasByes(bye_player[0]) > 0 and bye_index > 0):
            players.insert(bye_index, byePlayer)
            bye_index -= 1
            bye_player = players.pop(bye_index)
        pairings.insert(
            bye_index, (bye_player[0], bye_player[1], '-404', 'bye'))

    while (len(players) > 1):
        player1 = players.pop()
        player2 = players.pop()
        pairings.insert(0, (player1[0], player1[1], player2[0], player2[1]))

    return pairings
