-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

CREATE TABLE players (
	id serial primary key,
	name varchar(40)
);

CREATE TABLE matches (
	id serial primary key,
	winner_id int references players(id),
	loser_id int references players(id)
);

CREATE VIEW losers AS (
	SELECT loser_id, count(id) as losses
	FROM matches
	GROUP BY loser_id
	ORDER BY losses DESC
);

CREATE VIEW stats AS (
	SELECT p.id, p.name, count(m.winner_id) AS wins, count (m.id)  AS mcount
	FROM players p
	LEFT JOIN matches m ON p.id = m.winner_id 
	GROUP BY p.id 
	UNION
	SELECT p.id, p.name, 0 AS wins, count (m.loser_id) AS mcount
	FROM players p, losers m
	WHERE p.id = m.loser_id
	GROUP BY p.id
	ORDER BY wins DESC
);

CREATE VIEW standings AS (
	SELECT id, name, SUM(wins) as wins, SUM(mcount) as mcount 
	FROM stats
	GROUP BY id, name
	ORDER BY wins DESC
);
