from typing import Optional

from pydantic import BaseModel

# TODO: Add 2023-2024 teams
SHORT_TO_LONG_NAMES = {
    'Arsenal': 'Arsenal',
    'Aston Villa': 'Aston Villa',
    'Bournemouth': 'Bournemouth',
    'Brentford': 'Brentford',
    'Brighton': 'Brighton And Hove Albion',
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

LONG_TO_SHORT_NAMES = {
    'Arsenal': 'Arsenal',
    'Aston Villa': 'Aston Villa',
    'Bournemouth': 'Bournemouth',
    'Brentford': 'Brentford',
    'Brighton and Hove Albion': 'Brighton',
    'Burnley': 'Burnley',
    'Chelsea': 'Chelsea',
    'Crystal Palace': 'Crystal Palace',
    'Everton': 'Everton',
    'Fulham': 'Fulham',
    'Liverpool': 'Liverpool',
    'Luton Town': 'Luton',
    'Manchester City': 'Man City',
    'Manchester United': 'Man Utd',
    'Newcastle United': 'Newcastle',
    'Reading': 'Reading',
    'Sheffield United': 'Sheffield Utd',
    'Tottenham Hotspur': 'Spurs',
    'West Ham United': 'West Ham',
    'Wolverhampton Wanderers': 'Wolves',
    'Nottingham Forest': "Nott'm Forest",
}


class Team(BaseModel):
    short_name: Optional[str] = None
    long_name: Optional[str] = None
    position: Optional[int] = None
    points: Optional[int] = None

    def __init__(self, **data):
        # TODO: enforce that either short or long is present
        if data.get('long_name') is None:
            long_name = SHORT_TO_LONG_NAMES.get(data['short_name'])
            if long_name is None:
                # TODO - consider cases that we haven't mapped (should not be possible)
                long_name = data['short_name']
        else:
            long_name = data['long_name']

        if data.get('short_name') is None:
            short_name = LONG_TO_SHORT_NAMES.get(data['long_name'])
            if short_name is None:
                # TODO - consider cases that we haven't mapped (should not be possible)
                short_name = data['long_name']
        else:
            short_name = data['short_name']

        data.pop('short_name', None)
        data.pop('long_name', None)

        super().__init__(long_name=long_name, short_name=short_name, **data)
