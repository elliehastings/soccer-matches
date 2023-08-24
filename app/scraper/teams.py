# TODO: Make a scraper class for functionality?

import os
import re
from typing import Any

from fastapi import HTTPException, status as httpstatus
from aiohttp import ClientSession

from bs4 import BeautifulSoup

from app.models.teams import Team

PREMIER_LEAGUE_TABLE_URL = "https://www.premierleague.com/tables"
TEAM_NAME_CLASS = "league-table__team-name--long"
TEAM_POSITION_ROW_CLASS = "league-table__pos"
TEAM_POSITION_VALUE_CLASS = "league-table__value"
TEAM_POINTS_CLASS = "league-table__points"

# TODO: error handling for team scrape errors (need some valid error examples to know exception type)


def parse_teams(soup: BeautifulSoup) -> list[Team]:
    """
    Extracts an array of Teams from the teams table HTML page soup object
    """

    teams = []

    # Match all table rows with alpha/whitespace vals for
    # data-filtered-table-row-name (team names)
    team_rows = soup.find_all(
        'tr',
        attrs={
            "data-filtered-table-row-name": re.compile(r"^[A-Za-z\s\&]*$")}
    )

    for team_row in team_rows:
        name = team_row.find('span', class_=TEAM_NAME_CLASS)
        position = team_row.find('td', class_=TEAM_POSITION_ROW_CLASS).find(
            'span', class_=TEAM_POSITION_VALUE_CLASS)
        points = team_row.find('td', class_=TEAM_POINTS_CLASS)

        team = Team(
            long_name=name.get_text(),
            position=int(position.get_text()),
            points=int(points.get_text()),
        )

        teams.append(team)

    return teams


async def get():
    """
    Obtains team information by scraping the Premier League URL and parsing team data
    """
    async with ClientSession() as session:
        async with session.get(PREMIER_LEAGUE_TABLE_URL) as response:
            if response.status == 200:
                text = await response.text()
                soup = BeautifulSoup(markup=text, features='html.parser')
                team_rows = parse_teams(soup)

                return team_rows

            raise HTTPException(status_code=httpstatus.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Scrape error: received status code {response.status}")
