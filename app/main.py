from datetime import date, timedelta, datetime
from typing import Union, Annotated

from fastapi import FastAPI, HTTPException, Query, status as httpstatus
from starlette.responses import RedirectResponse

from app.scraper import teams, matches
from app.models.teams import Team
from app.models.matches import Match
from app.models.match_recommendations import MatchRecommendation
from app.recommender.recommender import RecommenderFactory

app = FastAPI()


@app.get("/")
async def root():
    response = RedirectResponse(url='/match-recommendations')
    return response


@app.get("/match-recommendations")
async def get_match_recommendations(
    start_date: Annotated[Union[date, None], Query()] = None,
    end_date: Annotated[Union[date, None], Query()] = None
) -> list[MatchRecommendation]:
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

    team_results = await teams.get()
    match_results = await matches.get(team_results)

    recommended_matches = RecommenderFactory.create_recommender(
        "MANUAL").recommend(match_results)

    return recommended_matches
