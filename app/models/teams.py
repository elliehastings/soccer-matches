from typing import List

from pydantic import BaseModel, ConfigDict

EXAMPLE_SCHEMA = {'name': 'Manchester City', 'position': 2, 'points': 6}


class Team(BaseModel):
    model_config = ConfigDict(json_schema_extra=EXAMPLE_SCHEMA)

    name: str
    position: int
    points: int
