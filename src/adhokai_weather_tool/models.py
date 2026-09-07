from pydantic import BaseModel, Field


class WeatherRequest(BaseModel):
    city: str = Field(..., description="The name of the city for which to fetch weather information.")

class WeatherResponse(BaseModel):
    condition: str = Field(..., description="Weather condition description.")
    temperature: float = Field(..., description="Current temperature in Celsius.")
    humidity: int = Field(..., description="Current humidity percentage.")