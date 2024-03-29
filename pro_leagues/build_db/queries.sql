CREATE TABLE IF NOT EXISTS game (
	game_id integer unique,
	game_date varchar,
	game_patch varchar,
	game_duration integer,
	b_team_id integer,
	r_team_id integer
);
CREATE TABLE IF NOT EXISTS game_team_picks (
	game_id integer,
	team_id integer,
	team_color integer,
	result integer,
	top_pick_id integer,
	jg_pick_id integer,
	mid_pick_id integer,
	adc_pick_id integer,
	sup_pick_id integer,
	ban_1 integer,
	ban_2 integer,
	ban_3 integer,
	ban_4 integer,
	ban_5 integer,
	unique(game_id,team_id)
);
CREATE TABLE IF NOT EXISTS game_team_stats (
	game_id integer,
	team_id integer,
	stat_type varchar,
	top varchar,
	jg varchar,
	mid varchar,
	adc varchar,
	sup varchar,
	unique(game_id,team_id,stat_type)
);
CREATE TABLE IF NOT EXISTS teams (
	team_id integer unique,
	team_name varchar,
	region varchar
);
CREATE TABLE IF NOT EXISTS champions (
	champion_id integer,
	champion_name varchar
);


