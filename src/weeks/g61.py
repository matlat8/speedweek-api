import httpx
from datetime import datetime, timezone
from typing import List, Dict, Any

def format_start_date(date: datetime) -> str:
    return date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

async def get_laps(car_id, track_id, start_date, garage_client: httpx.AsyncClient):
    url = f'/api/v1/laps?cars={car_id}&tracks={track_id}&after={format_start_date(start_date)}'
    async with garage_client as client:
        response = await client.get(url)
        if response.status_code != 200:
            print(response.content)
            response.raise_for_status()
        return response.json()