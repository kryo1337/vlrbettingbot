from fastapi import FastAPI
from scraper import vlr_upcoming_matches, vlr_live_score, vlr_match_results
from db import (
    insert_upcoming_matches,
    insert_live_scores,
    insert_match_results,
    get_events,
    create_event_leaderboard,
    list_available_events_for_creation,
    list_created_events,
    get_leaderboard,
    insert_bet,
    get_user_active_bets,
    get_event_matches,
)

app = FastAPI()


@app.get("/upcoming")
def insert_upcoming():
    data = vlr_upcoming_matches()
    insert_upcoming_matches(data)
    return {"message": "Upcoming matches inserted successfully", "data": data}


@app.get("/live")
def insert_live():
    data = vlr_live_score()
    insert_live_scores(data)
    return {"message": "Live scores inserted successfully", "data": data}


@app.get("/results")
def insert_results():
    data = vlr_match_results()
    insert_match_results(data)
    return {"message": "Match results inserted successfully", "data": data}


@app.get("/events")
def events():
    return get_events()


@app.post("/create/{match_event}")
def event_create(match_event: str):
    result = create_event_leaderboard(match_event)
    return result


@app.get("/available_events")
def available_events():
    data = vlr_upcoming_matches()
    insert_upcoming_matches(data)
    return list_available_events_for_creation()


@app.get("/created_events")
def created_events():
    return list_created_events()


@app.get("/leaderboard/{match_event}")
def leaderboard(match_event: str):
    return get_leaderboard(match_event)


@app.get("/event/{event_name}")
def event_matches(event_name: str):
    matches = get_event_matches(event_name)
    if not matches:
        raise HTTPException(
            status_code=404,
            detail=f"No upcoming matches found for event '{event_name}'.",
        )
    return {"message": f"Upcoming matches for event '{event_name}'", "data": matches}


@app.post("/bet")
def bet(bet_data: dict):
    """
    JSON:
    {
      "username": "DiscordNick",
      "match_id": 123,
      "event": "EventName",
      "predicted_winner": "Team1",
      "predicted_result": "1-2",
      "predicted_top_frag": "PlayerName"
    }
    """
    try:
        username = bet_data["username"]
        match_id = bet_data["match_id"]
        event = bet_data["event"]
        predicted_winner = bet_data["predicted_winner"]
        predicted_result = bet_data["predicted_result"]
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing field: {e}")

    predicted_top_frag = bet_data.get("predicted_top_frag")
    result = insert_bet(
        username,
        match_id,
        event,
        predicted_winner,
        predicted_result,
        predicted_top_frag,
    )
    return result


@app.get("/bets/{username}")
def bets(username: str):
    return get_user_active_bets(username)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
