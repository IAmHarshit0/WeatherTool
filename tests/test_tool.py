import os

import pytest

from adhokai_weather_tool import tool
from adhokai_weather_tool.models import WeatherResponse

API_KEY = os.getenv("OPENWEATHER_API_KEY")


def test_get_weather_live_api():
    if not API_KEY:
        pytest.skip("OPENWEATHER_API_KEY is not set in environment")

    result = tool.get_weather("Delhi")

    # Verify response schema types
    assert isinstance(result, WeatherResponse)
    assert isinstance(result.condition, str)
    assert isinstance(result.temperature, float)
    assert isinstance(result.humidity, int)


def test_get_weather_invalid_city():
    if not API_KEY:
        pytest.skip("OPENWEATHER_API_KEY is not set in environment")

    # Expect ValueError for nonexistent cities
    with pytest.raises(ValueError, match="City 'ThisCityDoesNotExist123' not found."):
        tool.get_weather("ThisCityDoesNotExist123")


def test_get_weather_missing_key(monkeypatch):
    # Temporarily clear the API key to test missing key error
    monkeypatch.setattr(tool, "OPENWEATHER_API_KEY", None)

    with pytest.raises(ValueError, match="OPENWEATHER_API_KEY is not configured"):
        tool.get_weather("Delhi")