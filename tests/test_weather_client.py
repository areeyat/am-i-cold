from unittest.mock import patch, MagicMock
import pytest
import requests

from src.weather_client import WeatherClient, WeatherClientError, DEFAULT_LONGITUDE, DEFAULT_LATITUDE, HOURLY_VARIABLES

def test_latitude_longitude_defaults():
    client = WeatherClient()

    assert client.latitude == DEFAULT_LATITUDE
    assert client.longitude == DEFAULT_LONGITUDE

def test_build_params():
    client = WeatherClient()
    params = client._build_params()

    assert params["latitude"] == DEFAULT_LATITUDE
    assert params["longitude"] == DEFAULT_LONGITUDE
    assert params["temperature_unit"] == "fahrenheit"
    assert params["wind_speed_unit"] == "mph"
    assert params["timezone"] == "America/Los_Angeles"
    assert params["hourly"] == ",".join(HOURLY_VARIABLES)

def test_fetch():
    return

def test_get_forecast_raw():
    return

def test_get_forecast_df():
    return

def test_raise_client_error():
    client = WeatherClient(max_retries=2, retry_delay=0)

    with patch("src.weather_client.requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError
        with pytest.raises(WeatherClientError):
            client._fetch()