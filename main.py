from datetime import date, timedelta
from typing import Union, Annotated

from fastapi import FastAPI, HTTPException, Query

from starlette.responses import RedirectResponse

app = FastAPI()


@app.get("/")
async def root():
    response = RedirectResponse(url='/fixture-recommendations')
    return response


@app.get("/fixture-recommendations")
async def get_fixture_recommendations(
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
            status_code=404, detail="Dates must be in present or future")

    return {"start_date": start_date, "end_date": end_date}
