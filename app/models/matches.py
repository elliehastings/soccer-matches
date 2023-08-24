from datetime import datetime

from pydantic import BaseModel

from app.models.teams import Team


class Match(BaseModel):
    display_date: str
    starts_at: datetime
    away_team: Team
    home_team: Team
