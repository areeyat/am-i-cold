import logging
import time

import pandas as pd
import requests

logger = logging.getLogger(__name__)

HOURLY_VARIABLES = [
    "temperature_2m",
    "apparent_temperature",
    "relativehumidity_2m",
    "windspeed_10m",
    "precipitation",
    "cloudcover",
    "precipitation_probability",
]

DEFAULT_LATITUDE = 47.57
DEFAULT_LONGITUDE = -122.39

class WeatherClient:
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    def __init__(
            self,
            latitude=DEFAULT_LATITUDE,
            longitude=DEFAULT_LONGITUDE,
            temperature_unit="fahrenheit",
            windspeed_unit="mph",
            timezone="America/Los_Angeles",
            max_retries=3,
            retry_delay=2.0,
            timeout=10,
    ):
        self.latitude = latitude
        self.longitude = longitude
        self.temperature_unit = temperature_unit
        self.windspeed_unit = windspeed_unit
        self.timezone = timezone
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.timeout = timeout
        
    def _build_params(self):
        return {
            "latitude" : self.latitude,
            "longitude": self.longitude,
            "hourly": ",".join(HOURLY_VARIABLES),
            "temperature_unit": self.temperature_unit,
            "windspeed_unit": self.windspeed_unit,
            "timzone": self.timezone,
        }