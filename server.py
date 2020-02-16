from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
from sqlalchemy import desc

from datetime import datetime
import os

# from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Restaurant, Offer

import requests


app = Flask(__name__)
app.secret_key = "b_xd3xf9095~xa68x90E^O1xd3R"

app.jinja_env.undefined = StrictUndefined



@app.route("/", methods=["GET"])
def index():
    """Show homepage."""

    return render_template("homepage.html")

@app.route("/map")
def search_location():
    """Search for your location on the map."""
    
    # Get user input from the search form
    query = request.args.get("location")

    req_tom = requests.get(f"https://api.tomtom.com/search/2/search/{query}.json?key=UEMHJeLAHMvvGsWGtxGl2NB9hNZXtpsm")
    search_results = req_tom.json()
    first_result = search_results.get("results")[1]
    lat_lon = first_result.get("position")
    
    return lat_lon


@app.route("/restaurant-object")
def get_restaurants_as_json():
    """Query database for restaurant info and send as JSON response."""

    # Query database and create dictionary
    restaurants = Restaurant.query.options(db.joinedload('offers')).all()
    rests = {}
    for rest in restaurants:
        rests[rest.name] = {'street_address': rest.street_address,
                            'city': rest.city,
                            'name': rest.name,
                            'state': rest.state,
                            'zipcode': rest.zipcode,
                            'email': rest.email}

        if rest.offers:
            offers = rest.offers
            first_offer = offers[0]
            rests[rest.name]['offer'] = first_offer.item

        if not rest.offers:
            rests[rest.name]['offer'] = " No current offers"

    print(rests)

    # Turn address into lat/lon using TomTom API
    for rest in rests.values():
        rest["address"] = f"{rest['street_address']} {rest['city']}, {rest['state']} {rest['zipcode']}"
        query = rest["address"]
        req_tom = requests.get(f"https://api.tomtom.com/search/2/search/{query}.json?key=UEMHJeLAHMvvGsWGtxGl2NB9hNZXtpsm")
        search_results = req_tom.json()
        first_result = search_results.get("results")[1]
        lat_lon = first_result.get("position")
        # Update dictionary with lat/lon
        rest["coordinate"] = [lat_lon["lon"], lat_lon["lat"]]

    return jsonify(rests)

    # Return jsonify(dictionary)


@app.route("/restaurant", methods=["GET"])
def show_login_form():
    """Show login form or registration button for restaurants."""

    restaurant_id = session.get("restaurant_id")

    if restaurant_id:
        return redirect(f"/restaurant-dashboard/{restaurant_id}")

    return render_template("restaurant-login.html")



@app.route("/restaurant", methods=["POST"])
def handle_login():
    """Login a restaurant user."""

    email = request.form.get("email")
    password = request.form.get("password")

    restaurant = Restaurant.query.filter_by(email=email).first()

    if not restaurant:
        flash(f"No account with {email}.")
        return redirect("/restaurant")

    if not restaurant.check_password(password):
        flash("Incorrect password.")
        return redirect("/restaurant")

    session["restaurant_id"] = restaurant.id
    flash("Login successful.")
    return redirect(f"/restaurant-dashboard/{restaurant.id}")


@app.route("/logout")
def logout():
    """Log out of a restaurant account."""

    if session.get("restaurant_id"):
        del session["restaurant_id"]
        flash("Logout successful.")
    
    return redirect("/")


@app.route("/register", methods=["GET"])
def show_registration_form():
    """Show registration form for restaurants."""

    return render_template("restaurant-register.html")


@app.route("/register", methods=["POST"])
def process_restaurant_registration():
    """Process restaurant registration."""
        
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    street_address = request.form.get("street-address")
    city = request.form.get("city")
    state = request.form.get("state")
    zipcode = request.form.get("zipcode")

    if Restaurant.query.filter_by(email=email).first():
        flash("An account with this email already exists.")
        return redirect("/register")

    new_restaurant = Restaurant(name=name,
                                email=email,
                                street_address=street_address,
                                city=city,
                                state=state,
                                zipcode=zipcode)

    new_restaurant.set_password(password)

    db.session.add(new_restaurant)
    db.session.commit()

    restaurant_id = new_restaurant.id

    # Log in new restaurant
    session["restaurant_id"] = restaurant_id

    flash(f"Successfully registered {name}.")
    return redirect(f"/restaurant-dashboard/{restaurant_id}")


@app.route("/restaurant-dashboard/<int:restaurant_id>")
def show_restaurant_dashboard(restaurant_id):
    """Show a restaurant's dashboard where they can view and edit offers."""

    if not check_authorization(restaurant_id):
        return render_template("unauthorized.html")

    restaurant = Restaurant.query.get(restaurant_id)
    offers = restaurant.offers

    return render_template("restaurant-dashboard.html",
                            restaurant=restaurant,
                            offers=offers)


@app.route("/restaurant-dashboard/<int:restaurant_id>/add-offer", methods=["POST"])
def add_offer(restaurant_id):
    """Add a new offer."""

    if not check_authorization(restaurant_id):
        return render_template("unauthorized.html")

    restaurant = Restaurant.query.get(restaurant_id)

    item = request.form.get("item")

    new_offer = Offer(restaurant_id=restaurant_id,
                      item=item)

    db.session.add(new_offer)
    db.session.commit()

    return redirect(f"/restaurant-dashboard/{restaurant_id}")


@app.route("/restaurant/delete/offer", methods=["POST"])
def delete_offer():
    """Delete an offer."""

    offer_id = request.form.get("offer")
    print(offer_id)

    offer = Offer.query.get(offer_id)
    print(offer)

    db.session.delete(offer)
    db.session.commit()

    return "Success"


def check_authorization(restaurant_id):
    """Check to see if the logged in restaurant is authorized to view page."""

    # Get the current user's id.
    user_id = session.get("restaurant_id")

    # If correct restaurant is not logged in, return False.
    if user_id != restaurant_id:
        return False

    return True


# Add jinja datetime filters to format datetime object in posts and comments.
def datetimeformat(value, format="%b %-d, %Y at %-I:%M %p"):
    return value.strftime(format)

app.jinja_env.filters['datetime'] = datetimeformat

def dateformat(value, format="%m-%d-%Y"):
    return value.strftime(format)

app.jinja_env.filters['date'] = dateformat

def htmldateformat(value, format="%Y-%m-%dT%H:%M"):
    return value.strftime(format)

app.jinja_env.filters['htmldatetime'] = htmldateformat


if __name__ == "__main__":
    app.debug = False
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    connect_to_db(app)
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
