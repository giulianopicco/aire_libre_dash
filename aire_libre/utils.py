from enum import Enum
import requests
from urllib.parse import urlencode
from datetime import datetime, timezone, timedelta

CONCENTRATIONS = [
    [0.0, 12.0],
    [12.1, 35.4],
    [35.5, 55.4],
    [55.5, 150.4],
    [150.5, 250.4],
    [250.5, 350.4],
    [350.5, 500.4],
]

BREAKPOINTS = [
    [0, 50],
    [51, 100],
    [101, 150],
    [151, 200],
    [201, 300],
    [301, 400],
    [401, 500],
]


def get_quality(pm2dot5_average):
    if pm2dot5_average is None:
        return (0)

    concentration = next(
        (c for c in CONCENTRATIONS if pm2dot5_average <= c[1]),
        CONCENTRATIONS[-1],
    )

    breakpoint_index = CONCENTRATIONS.index(concentration)
    breakpoint = BREAKPOINTS[breakpoint_index]

    try:
        index = int(
            ((breakpoint[1] - breakpoint[0]) /
             (concentration[1] - concentration[0]))
            * (pm2dot5_average - concentration[0])
            + breakpoint[0]
        )
    except Exception:
        index = None

    return index


def fetch(endpoint, source, days):
    now = datetime.now(timezone.utc)
    days_ago = now - timedelta(days=days)
    days_ago = days_ago.replace(hour=0, minute=0, second=0, microsecond=0)

    query = {
        "source": source,
        "start": days_ago.isoformat(),
        "end": now.isoformat(),
    }

    url = f"{endpoint}?{urlencode(query)}"
    response = requests.get(url)
    print(url)
    return response.json()


def fetch_data(source='6909e3', period=7):
    URL = 'https://rald-dev.greenbeep.com/api/v1/measurements'
    data = fetch(URL, source, period)
    return data


def fetch_stats(source='6909e3', period=7):
    URL = 'https://rald-dev.greenbeep.com/api/v1/stats'
    data = fetch(URL, source, period)
    return data
