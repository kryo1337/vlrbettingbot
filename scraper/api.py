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


@app.post("/event/{match_event}")
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
