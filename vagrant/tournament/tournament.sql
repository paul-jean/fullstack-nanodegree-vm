-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create table if not exists players (player_id smallserial primary key, name text);

create table if not exists matches (match_id smallserial primary key, winner_id integer references players (player_id), loser_id integer references players (player_id));

create or replace view wins_matches as
select coalesce(wins.winner_id, losses.loser_id) as player_id,
	coalesce(wins.num_wins, 0) as num_wins,
	(coalesce(losses.num_losses, 0) + coalesce(wins.num_wins, 0)) as num_matches from
	(select winner_id, count(*) as num_wins from matches group by winner_id) as wins
	full outer join
	(select loser_id, count(*) as num_losses from matches group by loser_id) as losses on
	wins.winner_id = losses.loser_id;

create or replace view standings as
select players.player_id, players.name, wins_matches.num_wins, wins_matches.num_matches from
players left join wins_matches
on players.player_id = wins_matches.player_id;

