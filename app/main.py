from datetime import timedelta, datetime
from pytz import timezone
from typing import Union, Annotated


from fastapi import FastAPI, HTTPException, Query, status as httpstatus
from starlette.responses import RedirectResponse

from app.scraper import teams, matches
from app.models.match_recommendations import MatchRecommendation
from app.recommender.recommender import RecommenderFactory

# Because our scraper runs in a browser set to EST the app only works with EST timezones
US_EASTERN_TZ = timezone('US/Eastern')

app = FastAPI()


@app.get("/")
async def root():
    response = RedirectResponse(url='/match-recommendations')
    return response


@app.get("/match-recommendations")
async def get_match_recommendations(
    start_date: Annotated[Union[datetime, None], Query()] = None,
    end_date: Annotated[Union[datetime, None], Query()] = None
) -> list[MatchRecommendation]:
    DEFAULT_DAY_RANGE = 3

    today_in_est = US_EASTERN_TZ.localize(datetime.today())
    today_start_est = today_in_est.replace(
        hour=0, minute=0, second=0, microsecond=0)
    today_end_est = today_start_est + timedelta(hours=24)

    if start_date is None:
        start_date_est = today_in_est
    else:
        start_date_est = start_date.astimezone(US_EASTERN_TZ)

    if end_date is None:
        end_date_est = US_EASTERN_TZ.localize(
            datetime.today()) + timedelta(days=DEFAULT_DAY_RANGE)
    else:
        end_date_est = end_date.astimezone(US_EASTERN_TZ)

    if start_date_est < today_start_est or end_date_est < today_end_est or end_date_est < start_date_est:
        raise HTTPException(
            status_code=httpstatus.HTTP_400_BAD_REQUEST,
            detail="Dates must be in present or future"
        )

    team_results = await teams.get()
    match_results = await matches.get(team_results, (start_date_est, end_date_est))

    recommended_matches = RecommenderFactory.create_recommender(
        "MANUAL").recommend(match_results)

    return recommended_matches
