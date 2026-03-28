from flask import Flask, render_template
from src.pipeline import *
from src.cold_score import *


app = Flask(__name__)

@app.route("/")
def home(): 
    
    cold_score = "soo cold"
    return render_template("index.html", if_cold = if_cold, cold_score = cold_score)

if __name__ == "__main__":
    app.run(debug=True)