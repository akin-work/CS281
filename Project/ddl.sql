CREATE TABLE IF NOT EXISTS Players (
    player_id   varchar(20),
    username    varchar(50),
    rank_level  varchar(10)  check (rank_level in ('Bronze','Silver','Gold','Platnium','Diamond')),
    country     varchar(30),
    join_date   varchar(25),
    Primary Key (player_id)

);
CREATE TABLE IF NOT EXISTS Teams (
    team_id varchar(30),
    team_name   varchar(25),
    region  varchar(5),
    created_date    varchar(4),
    coach_name  varchar(30),
    primary key(team_id)
);
CREATE TABLE IF NOT EXISTS Games (
    game_id varchar(15),
    game_name   varchar(30),
    genre   varchar(25),
    publisher   varchar(35),
    release_year    varchar(4),
    primary key(game_id)
);
CREATE TABLE IF NOT EXISTS Tournaments (
    tournament_id   varchar(15)
    tournament_name varcahr(35)
    coordinates varchar(50)
    starting_date   varchar(10)
    prize_pool  numeric (6,1)
    primary key(tournament_id)

);
CREATE TABLE IF NOT EXISTS Matches(
    match_id    varchar(15),
    tournament_id   varchar(15),
    game_id varchar(15),
    match_date  varchar(10),
    winner_team_id  varchar(30),
    primary key(match_id),
    foreign key(tournament_id) references Tournaments,
    foreign key(game_id) references Games,
    foreign key(winner_team_id) references Teams(team_id),
);
CREATE TABLE IF NOT EXISTS Team_participation(
    participation_id varchar(15)
    team_id     varchar(30),
    tournament_id   varchar(15),
    seed_number varchar(3),
    group_name  varchar(20),
    primary key(participation_id),
    foreign key(team_id) references Teams,
    foreign key(tournament_id) references Tournaments
);