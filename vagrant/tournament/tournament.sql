-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create table if not exists players (player_id smallserial primary key, name text);

create table if not exists matches (match_id smallserial primary key, winner_id integer references players (player_id), loser_id integer references players (player_id));
-- 
-- create view wins as
-- select players.player_id, players.name, count(matches.winner_id) as wins
-- from players left join matches
-- on players.player_id = matches.winner_id
-- group by matches.winner_id
-- order by wins;
-- 
-- create view losses as
-- select players.player_id, players.name, count(matches.loser_id) as losses
-- from players left join matches
-- on players.player_id = matches.loser_id
-- group by matches.loser)id
-- order by losses;
-- 
-- create view standings as
-- select player_id, wins.name, wins.wins as matches_won, losses.losses + wins.wins as total_matches
-- from wins join losses
-- on wins.player_id = losses.player_id
-- order by matches_won;
