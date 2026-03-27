import logging
from datetime import datetime, timezone

import pandas as pd
from sqlalchemy import create_engine, text

from weather_client import WeatherClient

logger = logging.getLogger(__name__)

DATABASE_URL = "sqlite:///data/weather.db"