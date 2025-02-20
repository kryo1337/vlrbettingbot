from connection import get_connection
from psycopg2 import sql


def insert_upcoming_matches(data):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM upcoming_matches;")

    insert_query = """
    INSERT INTO upcoming_matches (
        team1, team2, flag1, flag2, time_until_match,
        match_series, match_event, unix_timestamp, match_page
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
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
            ),
        )

    conn.commit()
    cur.close()
    conn.close()


def insert_live_scores(data):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM upcoming_matches;")

    insert_query = """
    INSERT INTO live_scores (
        team1, team2, flag1, flag2, team1_logo, team2_logo,
        score1, score2, team1_round_ct, team1_round_t,
        team2_round_ct, team2_round_t, map_number, current_map,
        time_until_match, match_event, match_series, unix_timestamp, match_page
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
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
            ),
        )

    conn.commit()
    cur.close()
    conn.close()


def insert_match_results(data):
    conn = get_connection()
    cur = conn.cursor()

    insert_query = """
    INSERT INTO match_results (
        team1, team2, score1, score2,
        flag1, flag2, time_completed, round_info,
        tournament_name, match_page, tournament_icon
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    for match in data["data"]:
        cur.execute(
            insert_query,
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
