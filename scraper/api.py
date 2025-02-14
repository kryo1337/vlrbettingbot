from fastapi import FastAPI
from scraper import vlr_upcoming_matches, vlr_live_score, vlr_match_results
from inserts import insert_upcoming_matches, insert_live_scores, insert_match_results

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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
