import requests
from urllib.parse import urlencode
from datetime import datetime, timezone, timedelta


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
    return response.json()


def fetch_data(source='6909e3', period=1):
    URL = 'https://rald-dev.greenbeep.com/api/v1/measurements'

    data = fetch(URL, source, period)
    return data
