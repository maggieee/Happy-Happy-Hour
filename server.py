"""TOMTOM challenge."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

# from model import connect_to_db, db

import json
import requests


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC" #? Is it always ABC?

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/search')
def search_stock_form():
    """Search stocks by symbol or key words and show realtime price."""

    # Get user input from the search form
    # location = request.args.get('location')
    # print(location)

    # If the symbol is in the set of symbols/key words in the company names,
    # return stock realtime price from Alpha Vantage API
    # payload_rt = {'function': 'TIME_SERIES_INTRADAY',  
    #            'symbol': symbol,
    #            'interval': '60min',
    #            'outputsize': 'compact',
    #            'apikey': 'PVW38W9JBAXB0XGX'}
    # # print(payload)
    # req_realtime = requests.get("https://www.alphavantage.co/query", params=payload_rt)
    # # print(req.url)
    # js_data_rt = req_realtime.json()
    # # print(js_data)
    
    # hourly_series_dict = js_data_rt.get('Time Series (60min)', 0)
    # # print(hourly_series_dict)

    # # print("#################################################")
    
    # middle_key = list(hourly_series_dict.keys())[0]
    # # print(middle_key)

    # price = hourly_series_dict.get(middle_key, 0).get('4. close', 0)
    # # print(price)
    # # and company name data from Edgar Online API.
    # # Else,...
    # print("\n\n####################symbol,price working#######################")
    # ema = display_daily_ema_chart(symbol)
    # print(ema)
    # return render_template("homepage.html", location=location)
    return render_template("homepage.html")



###############################################################################
if __name__ == "__main__":

    app.debug = True

    # connect_to_db(app)
    #? Why do you need it in all model, server and seed?

    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")