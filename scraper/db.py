from connection import get_connection
from psycopg2 import sql


def insert_upcoming_matches(data):
    conn = get_connection()
    cur = conn.cursor()

    insert_query = """
    INSERT INTO upcoming_matches (
        team1, team2, flag1, flag2, time_until_match,
        match_series, match_event, unix_timestamp, match_page, players
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (match_page) DO UPDATE SET
        team1 = EXCLUDED.team1,
        team2 = EXCLUDED.team2,
        flag1 = EXCLUDED.flag1,
        flag2 = EXCLUDED.flag2,
        time_until_match = EXCLUDED.time_until_match,
        match_series = EXCLUDED.match_series,
        match_event = EXCLUDED.match_event,
        unix_timestamp = EXCLUDED.unix_timestamp,
        players = EXCLUDED.players;
    """

    for match in data["data"]:
        cur.execute(
            insert_query,
            (
                match.get("team1"),
                match.get("team2"),
                match.get("flag1"),
                match.get("flag2"),
                match.get("time_until_match"),
                match.get("match_series"),
                match.get("match_event"),
                match.get("unix_timestamp"),
                match.get("match_page"),
                match.get("players", []),
            ),
        )

    conn.commit()
    cur.close()
    conn.close()


def insert_live_scores(data):
    conn = get_connection()
    cur = conn.cursor()

    insert_query = """
    INSERT INTO live_scores (
        team1, team2, flag1, flag2, team1_logo, team2_logo,
        score1, score2, team1_round_ct, team1_round_t,
        team2_round_ct, team2_round_t, map_number, current_map,
        time_until_match, match_event, match_series, unix_timestamp, match_page, players
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (match_page) DO UPDATE SET
        team1 = EXCLUDED.team1,
        team2 = EXCLUDED.team2,
        flag1 = EXCLUDED.flag1,
        flag2 = EXCLUDED.flag2,
        team1_logo = EXCLUDED.team1_logo,
        team2_logo = EXCLUDED.team2_logo,
        score1 = EXCLUDED.score1,
        score2 = EXCLUDED.score2,
        team1_round_ct = EXCLUDED.team1_round_ct,
        team1_round_t = EXCLUDED.team1_round_t,
        team2_round_ct = EXCLUDED.team2_round_ct,
        team2_round_t = EXCLUDED.team2_round_t,
        map_number = EXCLUDED.map_number,
        current_map = EXCLUDED.current_map,
        time_until_match = EXCLUDED.time_until_match,
        match_event = EXCLUDED.match_event,
        match_series = EXCLUDED.match_series,
        unix_timestamp = EXCLUDED.unix_timestamp,
        players = EXCLUDED.players;
    """

    for match in data["data"]:
        cur.execute(
            insert_query,
            (
                match.get("team1"),
                match.get("team2"),
                match.get("flag1"),
                match.get("flag2"),
                match.get("team1_logo"),
                match.get("team2_logo"),
                match.get("score1"),
                match.get("score2"),
                match.get("team1_round_ct"),
                match.get("team1_round_t"),
                match.get("team2_round_ct"),
                match.get("team2_round_t"),
                match.get("map_number"),
                match.get("current_map"),
                match.get("time_until_match"),
                match.get("match_event"),
                match.get("match_series"),
                match.get("unix_timestamp"),
                match.get("match_page"),
                match.get("players", []),
            ),
        )

    conn.commit()
    cur.close()
    conn.close()


def insert_match_results(data):
    conn = get_connection()
    cur = conn.cursor()

    insert_match_query = """
    INSERT INTO match_results (
        team1, team2, score1, score2, flag1, flag2, time_completed,
        round_info, tournament_name, match_page, tournament_icon,
        top_killer_name, top_killer_kills
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (match_page) DO UPDATE SET
        team1 = EXCLUDED.team1,
        team2 = EXCLUDED.team2,
        score1 = EXCLUDED.score1,
        score2 = EXCLUDED.score2,
        flag1 = EXCLUDED.flag1,
        flag2 = EXCLUDED.flag2,
        time_completed = EXCLUDED.time_completed,
        round_info = EXCLUDED.round_info,
        tournament_name = EXCLUDED.tournament_name,
        tournament_icon = EXCLUDED.tournament_icon,
        top_killer_name = EXCLUDED.top_killer_name,
        top_killer_kills = EXCLUDED.top_killer_kills
    RETURNING id;
    """

    insert_player_query = """
    INSERT INTO match_players (
        match_id, player_name, kills
    )
    VALUES (%s, %s, %s)
    ON CONFLICT DO NOTHING;
    """

    for match in data["data"]:
        cur.execute(
            insert_match_query,
            (
                match.get("team1"),
                match.get("team2"),
                match.get("score1"),
                match.get("score2"),
                match.get("flag1"),
                match.get("flag2"),
                match.get("time_completed"),
                match.get("round_info"),
                match.get("tournament_name"),
                match.get("match_page"),
                match.get("tournament_icon"),
                (
                    match["players"]["top_killer"]["player_name"]
                    if match.get("players")
                    else None
                ),
                (
                    match["players"]["top_killer"]["kills"]
                    if match.get("players")
                    else None
                ),
            ),
        )
        match_id = cur.fetchone()[0]

        if match.get("players") and "players" in match["players"]:
            for player in match["players"]["players"]:
                cur.execute(
                    insert_player_query,
                    (
                        match_id,
                        player["player_name"],
                        player["kills"],
                    ),
                )

    conn.commit()
    cur.close()
    conn.close()


def get_events():
    conn = get_connection()
    cur = conn.cursor()

    query = """
    SELECT 
        match_event, 
        json_agg(row_to_json(upcoming_matches)) AS matches
    FROM upcoming_matches
    GROUP BY match_event;
    """
    cur.execute(query)
    events = cur.fetchall()
    cur.close()
    conn.close()

    event_list = []
    for event in events:
        event_list.append({"event": event[0], "matches": event[1]})

    return {"message": "Events retrieved successfully", "data": event_list}


def list_available_events_for_creation():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT DISTINCT match_event FROM upcoming_matches;")
    rows = cur.fetchall()
    upcoming_events = [row[0] for row in rows]

    cur.execute("SELECT tablename FROM pg_tables WHERE tablename LIKE 'leaderboard_%';")
    rows2 = cur.fetchall()
    existing_leaderboards = [row[0] for row in rows2]

    available_events = [
        event
        for event in upcoming_events
        if f"leaderboard_{event}" not in existing_leaderboards
    ]

    cur.close()
    conn.close()

    return {
        "message": "Available events retrieved successfully",
        "data": available_events,
    }


def create_event_leaderboard(match_event):
    table_name = f"leaderboard_{match_event}"

    conn = get_connection()
    cur = conn.cursor()

    query = sql.SQL(
        "CREATE TABLE IF NOT EXISTS {} (username TEXT PRIMARY KEY, points INTEGER NOT NULL DEFAULT 0);"
    ).format(sql.Identifier(table_name))

    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()

    return {"message": f"Leaderboard for event '{match_event}' created successfully."}


def get_leaderboard(match_event):
    table_name = f"leaderboard_{match_event}"
    conn = get_connection()
    cur = conn.cursor()

    query = sql.SQL(
        "SELECT username, points FROM {} ORDER BY points DESC LIMIT 10;"
    ).format(sql.Identifier(table_name))

    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    leaderboard = [{"username": row[0], "points": row[1]} for row in rows]
    return {"message": f"Leaderboard for event '{match_event}'", "data": leaderboard}


def list_created_events():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT tablename FROM pg_tables WHERE tablename LIKE 'leaderboard_%';")
    rows = cur.fetchall()
    created_events = [row[0].replace("leaderboard_", "") for row in rows]

    cur.close()
    conn.close()

    return {"message": "Created events retrieved successfully", "data": created_events}


def insert_bet(
    username,
    match_id,
    event,
    predicted_winner,
    predicted_result,
    predicted_top_frag=None,
):
    conn = get_connection()
    cur = conn.cursor()
    query = """
    INSERT INTO bets (username, match_id, event, predicted_winner, predicted_result, predicted_top_frag)
    VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING id;
    """
    cur.execute(
        query,
        (
            username,
            match_id,
            event,
            predicted_winner,
            predicted_result,
            predicted_top_frag,
        ),
    )
    bet_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Bet placed successfully", "bet_id": bet_id}


def get_user_active_bets(username):
    conn = get_connection()
    cur = conn.cursor()
    query = """
    SELECT b.id, b.match_id, b.event, b.predicted_winner, b.predicted_result, b.predicted_top_frag, b.bet_time
    FROM bets b
    WHERE b.username = %s AND b.settled = FALSE;
    """
    cur.execute(query, (username,))
    rows = cur.fetchall()
    bets = []
    for row in rows:
        bets.append(
            {
                "bet_id": row[0],
                "match_id": row[1],
                "event": row[2],
                "predicted_winner": row[3],
                "predicted_result": row[4],
                "predicted_top_frag": row[5],
                "bet_time": row[6],
            }
        )
    cur.close()
    conn.close()
    return {"message": "Active bets retrieved successfully", "data": bets}


def get_event_matches(event_name: str):
    conn = get_connection()
    cur = conn.cursor()
    query = "SELECT * FROM upcoming_matches WHERE TRIM(match_event) = %s;"
    cur.execute(query, (event_name.strip(),))
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    matches = [dict(zip(columns, row)) for row in rows]
    cur.close()
    conn.close()
    return matches


def get_match_teams(match_id: int):
    conn = get_connection()
    cur = conn.cursor()
    query = "SELECT team1, team2 FROM upcoming_matches WHERE id = %s;"
    cur.execute(query, (match_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return {"team1": row[0], "team2": row[1]}
    else:
        return None


def get_available_event_matches(username: str, event_name: str):
    conn = get_connection()
    cur = conn.cursor()
    query = """
    SELECT * FROM upcoming_matches
    WHERE TRIM(match_event) = %s
      AND id NOT IN (
          SELECT match_id FROM bets WHERE username = %s AND settled = FALSE
      );
    """
    cur.execute(query, (event_name.strip(), username))
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    matches = [dict(zip(columns, row)) for row in rows]
    cur.close()
    conn.close()
    return matches


def get_match_players(match_id: int):
    conn = get_connection()
    cur = conn.cursor()

    query_upcoming = "SELECT players FROM upcoming_matches WHERE id = %s;"
    cur.execute(query_upcoming, (match_id,))
    row = cur.fetchone()
    if row and row[0]:
        cur.close()
        conn.close()
        return row[0]

    # query_live = "SELECT players FROM live_scores WHERE id = %s;"
    # cur.execute(query_live, (match_id,))
    # row = cur.fetchone()
    # if row and row[0]:
    #     cur.close()
    #     conn.close()
    #     return row[0]

    cur.close()
    conn.close()
    return []
