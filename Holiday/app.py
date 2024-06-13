from flask import Flask, render_template, request, jsonify
from flask import redirect, url_for, flash
from dotenv import load_dotenv
from geminiai import generate_itinerary,get_weather_data
import datetime
import os
import requests

app = Flask(__name__)
load_dotenv()
wapi_key = os.environ.get("api_key")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/places')
def places():
    return render_template('place.html')

@app.route('/itinerary', methods=['POST'])
def itinerary():
    source = request.form['source']
    destination = request.form['destination']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    no_of_day = (datetime.datetime.strptime(end_date, "%Y-%m-%d") - datetime.datetime.strptime(start_date, "%Y-%m-%d")).days
    if no_of_day < 0:
        flash("Return date should be greater than the Travel date (Start date).", "danger")
        return redirect(url_for("home"))
    #else:
        try:
            weather_data = get_weather_data(wapi_key, destination, start_date, end_date)
        except requests.exceptions.RequestException as e:
            flash("Error in retrieving weather data.{e.Error}", "danger")
            return redirect(url_for("home"))

    itinerary_text = generate_itinerary(source, destination, start_date, end_date, no_of_day)
    return render_template('itinerary.html', itinerary=itinerary_text)

if __name__ == '__main__':
    app.run(debug=True)
