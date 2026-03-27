import logging
from datetime import datetime, timezone

import pandas as pd
from sqlalchemy import create_engine, text

from weather_client import WeatherClient

logger = logging.getLogger(__name__)

DATABASE_URL = "sqlite:///data/weather.db"

def create_tables(engine):
    create_sql = text("""
        CREATE TABLE IF NOT EXISTS raw_weather_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fetched_at TEXT NOT NULL,
            forecast_time TEXT NOT NULL,
            latitude REAL,
            longitude REAL,
            temperature_f REAL,
            apparent_temp_f REAL,
            humidity_pct REAL,
            windspeed_mph REAL,
            precipitation_in REAL,
            cloud_cover_pct REAL,
            precip_probability_pct REAL,
            raw_json TEXT
        )
    """)

    with engine.connect() as conn:
        conn.execute(create_sql)
        conn.commit() # sqlalchemy doesn't auto-commit
        logger.info("Tables created (if they didn't exist)")

def load_slow(conn, df):
    conn.execute(text("TRUNCATE TABLE raw_weather_readings"))

    logger.info("starting slow loader ...")

    insert_clause = text("INSERT INTO raw_weather_readings VALUES \
                         (:fetched_at, :forecast_time, :latitude, :longitude, \
                         :temperature_f, :apparent_temp_f, :humidity_pct, \
                         :windspeed_mph, :precipitation_in, :cloud_cover_pct, \
                         :precip_probability_pct, :raw_json);")
    
    
    
    return
def load_fast():
    return
