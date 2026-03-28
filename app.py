from flask import Flask, render_template
from src.pipeline import *
from src.cold_score import *


app = Flask(__name__)

@app.route("/")
def home(): 
    weather_data = fetch_weather_data()
    cold_score = weather_data.apply(lambda x: get_cold_score(x.temperature_f), axis=1)
    cold_score_now = cold_score[8]
    if_cold = "yes"
    if cold_score_now == "not cold":
        if_cold = "no"

    return render_template("index.html", if_cold = if_cold, cold_score = cold_score_now)

if __name__ == "__main__":
    app.run(debug=True)