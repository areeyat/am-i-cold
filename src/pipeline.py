import logging
from datetime import datetime, timezone
import time

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
            precip_probability_pct REAL
        )
    """)

    with engine.connect() as conn:
        conn.execute(create_sql)
        conn.commit() # sqlalchemy doesn't auto-commit
        logger.info("Tables created (if they didn't exist)")

def load_slow(conn, client):

    # maybe get rid of this later if i decide to keep historical data?
    conn.execute(text("TRUNCATE TABLE raw_weather_readings"))
    conn.commit()

    logger.info("emptied table.")

    raw = client.get_forecast_raw()
    df = client.get_forecast_df()
    fetched_at = datetime.now()

    insert_clause = text("INSERT INTO raw_weather_readings VALUES \
                         (:fetched_at, :forecast_time, :latitude, :longitude, \
                         :temperature_f, :apparent_temp_f, :humidity_pct, \
                         :windspeed_mph, :precipitation_in, :cloud_cover_pct, \
                         :precip_probability_pct);")
    
    start_time = time.time()
    logger.info("starting slow loader ...")

    row_count = 0

    for row in df.itertuples():
        forecast_time = row.time
        latitude = raw['latitude']
        longitude = raw['longitude'] 
        temperature_f = row.temperature_2m
        apparent_temp_f = row.apparent_temperature
        humidity_pct = row.relativehumidity_2m # wait is this right? 
        windspeed_mph = row.windspeed_10m
        precipitation_in = row.precipitation
        cloud_cover_pct = row.cloudcover
        precip_probability_pct = row.precipitation_probability

        conn.execute(insert_clause, {"fetched_at": fetched_at,
                                     "forecast_time": forecast_time,
                                     "latitude": latitude,
                                     "longitude": longitude,
                                     "temperature_f": temperature_f,
                                     "apparent_temp_f": apparent_temp_f,
                                     "humidity_pct": humidity_pct,
                                     "windspeed_mph": windspeed_mph,
                                     "precipitation_in": precipitation_in,
                                     "cloud_cover_pct": cloud_cover_pct,
                                     "precip_probability_pct": precip_probability_pct})

        row_count += 1

    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info("loaded %d rows in %.2f seconds", row_count, elapsed_time)
    
    
def load_fast():
    return
