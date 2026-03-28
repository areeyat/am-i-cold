import numpy as np
import pandas as pd
from sqlalchemy import create_engine, text 
from pipeline import DATABASE_URL


def get_cold_score(temp):
    if temp > 72: 
        return "not cold"
    elif temp > 65:
        return "chilly"
    else:
        return "soo cold"
    
def fetch_weather_data():
    engine = create_engine(DATABASE_URL)

    with engine.connect() as conn:
        fetch_sql = text(""" 
            SELECT * FROM raw_weather_readings
        """)
        data = conn.execute(fetch_sql)
    return data

if __name__ == "__main__":
    weather_data = fetch_weather_data().all()
    print(pd.DataFrame(weather_data))
    

