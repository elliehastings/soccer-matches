# TODO: Make a scraper class for functionality?

import os
import re
from typing import Any

from fastapi import HTTPException, status as httpstatus
from aiohttp import ClientSession

from bs4 import BeautifulSoup

PREMIER_LEAGUE_TABLE_URL = "https://www.premierleague.com/tables"
TEAM_NAME_CLASS = "league-table__team-name--long"
TEAM_POSITION_ROW_CLASS = "league-table__pos"
TEAM_POSITION_VALUE_CLASS = "league-table__value"
TEAM_POINTS_CLASS = "league-table__points"

# TODO: proper type with schema for Team
# TODO: error handling for team scrape errors


def parse_teams(soup: BeautifulSoup) -> list[Any]:
    """
    Extracts an array of teams from the teams HTML page soup object

    For example:
    [{'club': 'Manchester City', 'position': 2, 'points': 6}, {'club': 'Brentford', 'position': 3, 'points': 4}]
    """

    teams = []

    # Match all table rows with alpha/whitespace vals for
    # data-filtered-table-row-name (team names)
    team_rows = soup.find_all(
        'tr',
        attrs={
            "data-filtered-table-row-name": re.compile(r"^[A-Za-z\s]*$")}
    )

    for team_row in team_rows:
        club = team_row.find('span', class_=TEAM_NAME_CLASS)
        position = team_row.find('td', class_=TEAM_POSITION_ROW_CLASS).find(
            'span', class_=TEAM_POSITION_VALUE_CLASS)
        points = team_row.find('td', class_=TEAM_POINTS_CLASS)

        team = {
            "club": club.get_text(),
            "position": int(position.get_text()),
            "points": int(points.get_text()),
        }

        teams.append(team)

    return teams


# TODO: typing
async def get():
    """
    Obtains team information by scraping the Premier League URL and parsing team data
    """
    async with ClientSession() as session:
        async with session.get(PREMIER_LEAGUE_TABLE_URL) as response:
            text = await response.text()

            if response.status == 200:
                soup = BeautifulSoup(markup=text, features='html.parser')
                team_rows = parse_teams(soup)

                # TESTING: print teams
                print(team_rows)

                return

            raise HTTPException(status_code=httpstatus.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Scrape error: received status code {response.status}")
