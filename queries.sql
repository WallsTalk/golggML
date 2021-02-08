CREATE TABLE IF NOT EXISTS game (
	game_id integer,
	game_date varchar,
	game_patch varchar,
	game_duration integer,
	b_team_id integer,
	r_team_id integer,
);

CREATE TABLE IF NOT EXISTS game_teams_picks (
	game_id integer,
	team_id integer,
	team_color varchar,
	result integer,
	top_pick_id integer,
	jg_pick_id integer,
	mid_pick_id integer,
	bot_pick_id integer,
	sup_pick_id integer,
	ban_1 integer,
	ban_2 integer,
	ban_3 integer,
	ban_4 integer,
	ban_5 integer
);

CREATE TABLE IF NOT EXISTS game_teams_distribution (
	game_id integer,
	team_id integer,
	dist_type varchar,
	top float,
	jg float,
	mid float,
	bot float,
	sup float
);


CREATE TABLE IF NOT EXISTS team (
	team_id integer,
	team_name varchar,
	region_id varchar
);

CREATE TABLE IF NOT EXISTS region (
	region_id integer,
	region_name varchar
);

CREATE TABLE IF NOT EXISTS champions (
	champion_id integer,
	champion_name varchar
);


