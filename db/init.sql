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
    match_page TEXT
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
    match_page TEXT
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
    match_page TEXT,
    tournament_icon TEXT
);

CREATE TABLE IF NOT EXISTS leaderboard (
    username TEXT PRIMARY KEY,
    points INTEGER NOT NULL DEFAULT 0
);

