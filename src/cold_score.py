import numpy as np
import pandas as pd
from sqlalchemy import create_engine, text 
from pipeline import fetch_weather_data


def get_cold_score(temp):
    if temp > 72: 
        return "not cold"
    elif temp > 65:
        return "chilly"
    else:
        return "soo cold"

if __name__ == "__main__":
    weather_data = fetch_weather_data()
    print(weather_data.columns)
    print(weather_data['temperature_f'])

    

