import os

import requests
from dotenv import load_dotenv

from .models import WeatherRequest, WeatherResponse

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city: str) -> WeatherResponse:
    """Fetch current weather for a city using OpenWeatherMap API and return structured response.

    Args:
        city: The name of the city (e.g., 'Delhi', 'London').
    """
    # Validate input using Pydantic model
    request = WeatherRequest(city=city)

    if not OPENWEATHER_API_KEY:
        raise ValueError("OPENWEATHER_API_KEY is not configured in environment variables.")

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": request.city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
    }

    response = requests.get(url, params=params, timeout=5)

    if response.status_code == 404:
        raise ValueError(f"City '{request.city}' not found.")
    elif response.status_code != 200:
        raise RuntimeError(f"Weather service error (Status Code: {response.status_code})")

    data = response.json()

    return WeatherResponse(
        condition=data["weather"][0]["description"].capitalize(),
        temperature=data["main"]["temp"],
        humidity=data["main"]["humidity"],
    )