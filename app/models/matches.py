from typing import List
from datetime import datetime

from dateutil import parser

from pydantic import BaseModel, ConfigDict


EXAMPLE_SCHEMA = {'display_date': 'Monday 21 August 2023', 'starts_at': parser.parse(
    "Monday 21 August 2023 15:00"), 'away_team': 'Arsenal', 'home_team': 'Crystal Palace'}

# TODO: Add 2023-2024 teams
SHORT_TO_LONG_NAMES = {
    'Arsenal': 'Arsenal',
    'Aston Villa': 'Aston Villa',
    'Bournemouth': 'Bournemouth',
    'Brentford': 'Brentford',
    'Brighton': 'Brighton & Hove Albion',
    'Burnley': 'Burnley',
    'Chelsea': 'Chelsea',
    'Crystal Palace': 'Crystal Palace',
    'Everton': 'Everton',
    'Fulham': 'Fulham',
    'Liverpool': 'Liverpool',
    'Luton': 'Luton Town',
    'Man City': 'Manchester City',
    'Man Utd': 'Manchester United',
    'Newcastle': 'Newcastle United',
    'Reading': 'Reading',
    'Sheffield Utd': 'Sheffield United',
    'Spurs': 'Tottenham Hotspur',
    'West Ham': 'West Ham United',
    'Wolves': 'Wolverhampton Wanderers',
    "Nott'm Forest": 'Nottingham Forest',
}


class Match(BaseModel):
    model_config = ConfigDict(json_schema_extra=EXAMPLE_SCHEMA)

    display_date: str
    starts_at: datetime
    away_team: str
    home_team: str


def format_names_to_long(match: Match) -> Match:
    '''
    Accepts a Match object with team names in short format and returns
    a new Match object with team names in long format to enable
    comparison with the long names in Team objects

    Example:
    Match(
      display_date='Saturday 2 September 2023',
      starts_at=datetime.datetime(2023, 9, 2, 10, 0, tzinfo=tzlocal()),
      away_team="Nott'm Forest",
      home_team='Chelsea'
    ) ->
    Match(
      display_date='Saturday 2 September 2023',
      starts_at=datetime.datetime(2023, 9, 2, 10, 0, tzinfo=tzlocal()),
      away_team='Nottingham Forest',
      home_team='Chelsea'
    )
    '''

    away_team_long = SHORT_TO_LONG_NAMES.get(match.away_team)
    if away_team_long is None:
        # TODO - consider cases that we haven't mapped (should not be possible)
        away_team_long = match.away_team

    home_team_long = SHORT_TO_LONG_NAMES.get(match.home_team)
    if home_team_long is None:
        # TODO - consider cases that we haven't mapped (should not be possible)
        home_team_long = match.home_team

    return Match(
        display_date=match.display_date,
        starts_at=match.starts_at,
        away_team=away_team_long,
        home_team=home_team_long,
    )
