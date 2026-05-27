import pandas as pd
from flask import Flask, render_template
from src.pipeline import refresh_weather_data
from src.cold_score import get_cold_score


app = Flask(__name__)

@app.route("/")
def home():
    weather_data = refresh_weather_data()
    weather_data["forecast_time"] = pd.to_datetime(weather_data["forecast_time"])
    now = pd.Timestamp.now()
    closest_idx = (weather_data["forecast_time"] - now).abs().idxmin()
    temp_now = weather_data.loc[closest_idx, "temperature_f"]

    cold_score_now = get_cold_score(temp_now)
    if_cold = "no" if cold_score_now == "not cold" else "yes"

    return render_template("index.html", if_cold=if_cold, cold_score=cold_score_now)

if __name__ == "__main__":
    app.run(debug=True)