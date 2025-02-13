from connection import get_connection


def insert_upcoming_matches(data):
    conn = get_connection()
    cur = conn.cursor()

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
