from unittest.mock import patch, MagicMock

import pandas as pd
import pytest
from sqlalchemy import create_engine as real_create_engine

from src.pipeline import load_fast, refresh_weather_data

SAMPLE_RAW = {
    "latitude": 47.578,
    "longitude": -122.411,
    "hourly": {
        "time": ["2024-01-01T00:00", "2024-01-01T01:00"],
        "temperature_2m": [55.0, 57.0],
        "apparent_temperature": [50.0, 52.0],
        "relativehumidity_2m": [80.0, 75.0],
        "windspeed_10m": [5.0, 6.0],
        "precipitation": [0.0, 0.0],
        "cloudcover": [20.0, 25.0],
        "precipitation_probability": [10.0, 15.0],
        "is_day": [1, 1],
        "rain": [0.0, 0.0],
    },
}

SAMPLE_DF = pd.DataFrame.from_dict(SAMPLE_RAW["hourly"])


@pytest.fixture
def in_memory_engine():
    with patch("src.pipeline.create_engine") as mock:
        mock.return_value = real_create_engine("sqlite:///:memory:")
        yield mock


# --- load_fast ---

def test_load_fast_renames_columns(in_memory_engine):
    result = load_fast(SAMPLE_DF.copy(), SAMPLE_RAW)

    assert "forecast_time" in result.columns
    assert "temperature_f" in result.columns
    assert "apparent_temp_f" in result.columns
    assert "humidity_pct" in result.columns
    assert "windspeed_mph" in result.columns
    assert "precipitation_in" in result.columns
    assert "cloud_cover_pct" in result.columns
    assert "precip_probability_pct" in result.columns


def test_load_fast_adds_metadata(in_memory_engine):
    result = load_fast(SAMPLE_DF.copy(), SAMPLE_RAW)

    assert "fetched_at" in result.columns
    assert "latitude" in result.columns
    assert "longitude" in result.columns
    assert result["latitude"].iloc[0] == SAMPLE_RAW["latitude"]
    assert result["longitude"].iloc[0] == SAMPLE_RAW["longitude"]


def test_load_fast_preserves_row_count(in_memory_engine):
    result = load_fast(SAMPLE_DF.copy(), SAMPLE_RAW)

    assert len(result) == len(SAMPLE_DF)


def test_load_fast_writes_to_db(in_memory_engine):
    engine = in_memory_engine.return_value
    load_fast(SAMPLE_DF.copy(), SAMPLE_RAW)

    persisted = pd.read_sql("SELECT * FROM raw_weather_readings", engine)
    assert len(persisted) == len(SAMPLE_DF)
    assert "temperature_f" in persisted.columns


# --- refresh_weather_data ---

def test_refresh_weather_data_calls_api(in_memory_engine):
    with patch("src.pipeline.WeatherClient") as MockClient:
        MockClient.return_value.get_forecast_raw.return_value = SAMPLE_RAW
        refresh_weather_data()

    MockClient.return_value.get_forecast_raw.assert_called_once()


def test_refresh_weather_data_returns_dataframe(in_memory_engine):
    with patch("src.pipeline.WeatherClient") as MockClient:
        MockClient.return_value.get_forecast_raw.return_value = SAMPLE_RAW
        result = refresh_weather_data()

    assert isinstance(result, pd.DataFrame)
    assert len(result) == len(SAMPLE_DF)
    assert "temperature_f" in result.columns
