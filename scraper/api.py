import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import redis.asyncio as redis
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
    get_match_teams,
    get_available_event_matches,
    get_match_players,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = redis.from_url(
        "redis://redis:6379", encoding="utf-8", decode_responses=True
    )
    await FastAPILimiter.init(redis_client)
    yield
    await redis_client.close()


app = FastAPI(lifespan=lifespan)


@app.get("/upcoming", dependencies=[Depends(RateLimiter(times=250, seconds=60))])
def insert_upcoming():
    data = vlr_upcoming_matches()
    insert_upcoming_matches(data)
    return {"message": "Upcoming matches inserted successfully", "data": data}


@app.get("/live", dependencies=[Depends(RateLimiter(times=250, seconds=60))])
def insert_live():
    data = vlr_live_score()
    insert_live_scores(data)
    return {"message": "Live scores inserted successfully", "data": data}


@app.get("/results", dependencies=[Depends(RateLimiter(times=250, seconds=60))])
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


@app.get("/match/teams/{match_id}")
def match_teams(match_id: int):
    teams = get_match_teams(match_id)
    if not teams:
        raise HTTPException(status_code=404, detail="Match not found.")
    return {"message": "Teams retrieved successfully", "data": teams}


@app.get("/available_matches/{username}/{event_name}")
def available_matches(username: str, event_name: str):
    matches = get_available_event_matches(username, event_name)
    return {"message": f"Available matches for event '{event_name}'", "data": matches}


@app.get("/match/players/{match_id}")
def match_players(match_id: int):
    players = get_match_players(match_id)
    if not players:
        raise HTTPException(status_code=404, detail="No players found for this match.")
    return {"message": "Players retrieved successfully", "data": players}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
