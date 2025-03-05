CREATE TABLE IF NOT EXISTS upcoming_matches (
    id SERIAL PRIMARY KEY,
    team1 TEXT NOT NULL,
    team2 TEXT NOT NULL,
    flag1 TEXT,
    flag2 TEXT,
    time_until_match TEXT,
    match_series TEXT,
    match_event TEXT,
    unix_timestamp TIMESTAMP,
    match_page TEXT UNIQUE,
    players TEXT[]
);

CREATE TABLE IF NOT EXISTS live_scores (
    id SERIAL PRIMARY KEY,
    team1 TEXT NOT NULL,
    team2 TEXT NOT NULL,
    flag1 TEXT,
    flag2 TEXT,
    team1_logo TEXT,
    team2_logo TEXT,
    score1 INTEGER,
    score2 INTEGER,
    team1_round_ct TEXT,
    team1_round_t TEXT,
    team2_round_ct TEXT,
    team2_round_t TEXT,
    map_number TEXT,
    current_map TEXT,
    time_until_match TEXT,
    match_event TEXT,
    match_series TEXT,
    unix_timestamp TIMESTAMP,
    match_page TEXT UNIQUE,
    players TEXT[]
);

CREATE TABLE IF NOT EXISTS match_results (
    id SERIAL PRIMARY KEY,
    team1 TEXT NOT NULL,
    team2 TEXT NOT NULL,
    score1 INTEGER,
    score2 INTEGER,
    flag1 TEXT,
    flag2 TEXT,
    time_completed TEXT,
    round_info TEXT,
    tournament_name TEXT,
    match_page TEXT UNIQUE,
    tournament_icon TEXT,
    top_killer_name TEXT,
    top_killer_kills INTEGER
);

CREATE TABLE IF NOT EXISTS match_players (
    id SERIAL PRIMARY KEY,
    match_id INTEGER NOT NULL,
    player_name TEXT NOT NULL,
    kills INTEGER NOT NULL,
    FOREIGN KEY (match_id) REFERENCES match_results(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS leaderboard (
    username TEXT PRIMARY KEY,
    points INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS bets (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    match_id INTEGER NOT NULL,
    event TEXT NOT NULL,
    predicted_winner TEXT NOT NULL,
    predicted_result TEXT NOT NULL,
    predicted_top_frag TEXT NOT NULL,
    bet_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    settled BOOLEAN DEFAULT FALSE,
    UNIQUE (username, match_id),
    FOREIGN KEY (match_id) REFERENCES upcoming_matches(id)
);

