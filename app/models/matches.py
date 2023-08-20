from typing import List
from datetime import datetime

from dateutil import parser

from pydantic import BaseModel, ConfigDict


EXAMPLE_SCHEMA = {'display_date': 'Monday 21 August 2023', 'starts_at': parser.parse(
    "Monday 21 August 2023 15:00"), 'away_team': 'Arsenal', 'home_team': 'Crystal Palace'}


class Match(BaseModel):
    model_config = ConfigDict(json_schema_extra=EXAMPLE_SCHEMA)

    display_date: str
    starts_at: datetime
    away_team: str
    home_team: str
