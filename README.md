# About this app

A FastAPI server that serves up recommendations for upcoming Premier League football (as in, soccer football :soccer:) recommendations based on the ranking of the teams on the table.

There will be two options, a structured endpoint that applies the recommendation manually and an unstructured endpoint that returns the recommendation supplied by the OpenAI client.

Recommendations are based on either of two 'scores' (or possibly a combination!):

1. "Closeness": Minimum difference of team points (how close are the teams on the table, and therefore how close and exciting might the game be?)
2. "Quality": Maximum average of team points (how high up on the table are both teams?)

**Note**: this is a **work-in-progress** side project to play with FastAPI and OpenAI and is not meant for Production usage. Features are actively in development - see below for the running roadmap!

# Usage note

This app makes use of web scraping to power the match recommendation results.

This will ultimately be done at most a few times per day with the results cached to reduce hits to the scraped website to the minimum necessary and at or below standard human usage.

However, in the current state it fetches the data on a per-request basis (unless you write and load the results to/from a file in development, which is recommended).

:warning: As such any requests to the match-recommendations endpoint should be run with caution to avoid significant request load!

# Running the app

Run the server

```bash
uvicorn app.main:app --reload
```

Open the URL outputted by uvicorn in a browser

```
http://127.0.0.1:8000
http://127.0.0.1:8000/docs
```

or send curl commands to the endpoint directly

```
curl -X GET http://127.0.0.1:8000/match-recommendations?start_date=2023-08-19&end_date=2023-08-23
```

# TODO

Tracking project todos:

1.0 (proof of concept) - remaining:

* Add non-GPT API
* Handle matches in progress
* Date filtering - filter by input dates

1.1 (add AI, cleanup)

* Structure data to send to GPT
* Call GPT to get recommendations
* Return formatted recommendations
* Restrict date ranges or add pagination / infinite scroll
* Clean up quotes / add py linting

2.0

* Add models and persistent storage using SQLite
* Add background task to scrape table & fixtures for given dates once per day
* Cache API results so we're not webscraping once per API request :grimacing:

3.0

* Add simple UI (defaulting to requesting the next few days)

4.0

* envs/Docker/deploy

5.0

* Add custom UI with date filtering or other filters (league, etc)
