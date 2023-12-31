# TODO: Make a scraper class for functionality?
from datetime import date

from dateutil import parser
from dateutil.tz import gettz
from bs4 import BeautifulSoup
from fastapi import HTTPException, status as httpstatus

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.models.matches import Match
from app.models.teams import Team


PREMIER_LEAGUE_MATCHES_URL = "https://www.premierleague.com/fixtures"
COOKIES_ACCEPT_BUTTON_ID = "onetrust-accept-btn-handler"
ADVERTISEMENT_MODAL_CLOSE_ELEMENT_ID = "advertClose"
DATE_CONTAINER_CLASS = "fixtures__date-container"
MATCH_DATE_LONG_CLASS = "fixtures__date--long"
MATCH_FIXTURE_CLASS = "match-fixture"

# TODO: clean up / class-ify driver logic
# TODO: error handling for matches scrape errors (need some valid error examples to know exception type)


def initialize_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--incognito")
    options.add_argument("--headless")

    driver = webdriver.Chrome()
    driver.implicitly_wait(2)  # global wait seconds

    return driver


def fetch_static_matches_page(driver):
    driver.get(PREMIER_LEAGUE_MATCHES_URL)
    accept_cookies_button = driver.find_element(
        By.ID, COOKIES_ACCEPT_BUTTON_ID)
    accept_cookies_button.click()
    modal_close_element = driver.find_element(
        By.ID, ADVERTISEMENT_MODAL_CLOSE_ELEMENT_ID)

    try:
        # Advert modal not always visible/interactable ; sometimes present with display:none;
        WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located((By.ID, ADVERTISEMENT_MODAL_CLOSE_ELEMENT_ID)))

        modal_close_element.click()

        try:
            WebDriverWait(driver, 3).until(
                EC.invisibility_of_element_located((By.ID, ADVERTISEMENT_MODAL_CLOSE_ELEMENT_ID)))

            return driver.page_source
        except:
            raise HTTPException(status_code=httpstatus.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Scrape error: could not bypass advert modal")
    except:
        return driver.page_source


def parse_matches(soup: BeautifulSoup, teams: list[Team]) -> list[Match]:
    """
    Extracts an array of Matches from the Fixtures table HTML page soup object
    """

    matches = []

    # Match all date "rows" - div with date contains all matches for date
    date_sections = soup.find_all(
        'div',
        class_=DATE_CONTAINER_CLASS
    )

    # For each date, extract the matches and add date and flatmap them
    for date_section in date_sections:
        date_string = date_section.find(
            'time', class_=MATCH_DATE_LONG_CLASS).attrs['datetime']

        match_rows = date_section.find_all('li', class_=MATCH_FIXTURE_CLASS)
        for match_row in match_rows:
            away_team_short_name = match_row.attrs['data-away']
            home_team_short_name = match_row.attrs['data-home']

            teams_element = match_row.find(
                'span', class_="match-fixture__teams")

            match_start_time_elem = teams_element.find('time')
            # TODO: some matches can be in progress, in which case it shows the minutes!
            # For now we skip matches in progress
            if match_start_time_elem is None:
                continue

            # TODO: support other timezones
            match_start_time_string = match_start_time_elem.attrs['datetime']
            match_starts_at_date = parser.parse(
                date_string + " " + match_start_time_string + " EST",
                tzinfos={"EST": gettz("US/Eastern")}
            )

            away_team = Team(short_name=away_team_short_name)
            home_team = Team(short_name=home_team_short_name)

            for team in teams:
                if team.short_name == away_team_short_name:
                    away_team = team
                if team.short_name == home_team_short_name:
                    home_team = team

            match = Match(
                display_date=date_string,
                starts_at=match_starts_at_date,
                away_team=away_team,
                home_team=home_team
            )
            matches.append(match)

    return matches


async def get(teams: list[Team], date_range: tuple[date, date]) -> list[Match]:
    """
    Obtains matches information by scraping the Premier League URL and parsing team data
    """

    # Set up Selenium
    driver = initialize_driver()

    # Interact with page with Selenium to close ad modal
    page_source = fetch_static_matches_page(driver)

    soup = BeautifulSoup(markup=page_source, features='html.parser')
    matches = parse_matches(soup, teams)

    filtered_matches = [
        match for match in matches if match.starts_at > date_range[0] and match.starts_at < date_range[1]]

    return filtered_matches
