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

class WeatherClientError(Exception):
    pass

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
            "timezone": self.timezone,
        }
    
    def _fetch(self):
        params = self._build_params()

        for attempt in range(1, self.max_retries + 1):
            try:
                logger.info(
                    "Fetching wather data (attempt %d/%d)",
                    attempt,
                    self.max_retries,
                )
                response = requests.get(
                    self.BASE_URL, params=params, timeout=self.timeout
                )
                response.raise_for_status()

                data = response.json()
                logger.info("Successfully fetched weather data")
                return data 
            
            except requests.exceptions.Timeout:
                logger.warning("Request timed out (attempt %d/%d)", attempt, self.max_retries)
            except requests.exceptions.ConnectionError: 
                logger.warning("Connection error (attempt %d/%d)", attempt, self.max_retries)
            except requests.exceptions.HTTPError as e: 
                logger.warning("HTTP error %s (attempt %d/%d)", e.response.status_code, attempt, self.max_retries)

            if attempt < self.max_retries:
                wait_time = self.retry_delay * attempt # backoff
                logger.info("Retrying in %.1f seconds...", wait_time)
                time.sleep(wait_time)
        
        raise WeatherClientError(
            f"Failed to fetch weather data after {self.max_retries} attempts"
        )
