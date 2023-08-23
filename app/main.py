from datetime import date, timedelta
from typing import Union, Annotated

from fastapi import FastAPI, HTTPException, Query, status as httpstatus
from starlette.responses import RedirectResponse

from app.scraper import teams, matches

app = FastAPI()


@app.get("/")
async def root():
    response = RedirectResponse(url='/match-recommendations')
    return response


@app.get("/match-recommendations")
async def get_match_recommendations(
    start_date: Annotated[Union[date, None], Query()] = None,
    end_date: Annotated[Union[date, None], Query()] = None
):
    DEFAULT_DAY_RANGE = 3

    if start_date is None:
        start_date = date.today()
    if end_date is None:
        end_date = date.today() + timedelta(days=DEFAULT_DAY_RANGE)

    if start_date < date.today() or end_date < date.today() or end_date < start_date:
        raise HTTPException(
            status_code=httpstatus.HTTP_400_BAD_REQUEST,
            detail="Dates must be in present or future"
        )

    # TODO: Get teams and matches, collapse into one dataset, and feed to recommendation engine
    team_results = await teams.get()
    print("teams:\n")
    print(team_results)
    match_results = await matches.get(team_results)
    print("matches with teams:\n")
    print(match_results)

    return {"start_date": start_date, "end_date": end_date}
