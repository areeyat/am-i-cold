from flask import Flask, render_template, jsonify
from src.pipeline import *
from src.cold_score import *


app = Flask(__name__)

@app.route("/api/weather")
def weather(): 
    weather_data = fetch_weather_data()
    cold_score = weather_data.apply(lambda x: get_cold_score(x.temperature_f), axis=1)
    cold_score_past_hr = cold_score[7]
    cold_score_now = cold_score[8]
    cold_score_next_hr = cold_score[9]

    if_cold = "yes"
    if cold_score_now == "not cold":
        if_cold = "no"

    '''
    return render_template("index.html", if_cold = if_cold, cold_score = cold_score_now, 
                           last_hr_cold_score = cold_score_past_hr, next_hr_cold_score = cold_score_next_hr)

    '''
if __name__ == "__main__":
    app.run(debug=True)