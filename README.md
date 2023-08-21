# About this app

A FastAPI server that serves up recommendations for upcoming Premier League football (as in, soccer football ⚽️) recommendations based on the ranking of the teams on the table.

There will be two options, a structured endpoint that applies the recommendation manually and an unstructured endpoint that returns the recommendation supplied by the OpenAI client.

**Note**: this is a work-in-progress side project to play with FastAPI and OpenAI and is not meant for Production usage

# Usage note

This app makes use of web scraping to power the match recommendation results.

This will ultimately be done at most a few times per day with the results cached to reduce hits to the scraped website to the minimum necessary and at or below standard human usage.

However, in the current state it fetches the data on a per-request basis (unless you write and load the results to/from a file in development, which is recommended).

As such any requests to the match-recommendations endpoint should be run with caution to avoid significant request load!

# Running the app

Run the server

```bash
uvicorn app.main:app --reload
```

Open the provided URL in a browser or send curl commands to the URL

Ex:

```
curl -X GET http://127.0.0.1:8000/match-recommendations?start_date=2023-08-19&end_date=2023-08-23
```

# TODO

Tracking project todos:

1.0 (proof of concept) - remaining:

* Consolidate team and match data into one structure to use for recommendation
* Add non-GPT API
* Handle matches in progress

1.1 (add AI, cleanup)

* Structure data to send to GPT
* Call GPT to get recommendations
* Return formatted recommendations
* Restrict date ranges or add pagination / infinite scroll
* Clean up quotes / add py linting

2.0

* Add models and persistent storage using SQLite
* Add background task to scrape table & fixtures for given dates once per day
* Cache API results so we're not webscraping once per API request like monsters

3.0

* Add simple UI (defaulting to requesting the next few days)

4.0

* envs/Docker/deploy

5.0

* Add custom UI with date filtering or other filters (league, etc)
