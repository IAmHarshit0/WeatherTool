import pytest
from pydantic import ValidationError

from adhokai_weather_tool.models import WeatherRequest, WeatherResponse


def test_weather_request_valid():
    req = WeatherRequest(city="Delhi")
    assert req.city == "Delhi"


def test_weather_request_missing_city():
    with pytest.raises(ValidationError):
        WeatherRequest()


def test_weather_response_valid():
    res = WeatherResponse(condition="Sunny", temperature=25.0, humidity=50)
    assert res.condition == "Sunny"
    assert res.temperature == 25.0
    assert res.humidity == 50


def test_weather_response_invalid_type():
    with pytest.raises(ValidationError):
        WeatherResponse(condition="Sunny", temperature="not_a_number", humidity=50)