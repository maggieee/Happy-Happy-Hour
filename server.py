from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from sqlalchemy import desc

from datetime import datetime
import os

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Restaurant, Offer


app = Flask(__name__)
app.secret_key = "b_xd3xf9095~xa68x90E^O1xd3R"

app.jinja_env.undefined = StrictUndefined



@app.route("/", methods=["GET"])
def index():
    """Show homepage."""

    return render_template("homepage.html")


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
    quantity = request.form.get("quantity")
    price = request.form.get("price")
    start_time = request.form.get("start-time")
    end_time = request.form.get("end-time")


    new_offer = Offer(restaurant_id=restaurant_id,
                      item=item,
                      quantity=quantity,
                      price=price,
                      start_time=start_time,
                      end_time=end_time)

    db.session.add(new_offer)
    db.session.commit()

    return redirect(f"/restaurant-dashboard/{restaurant_id}")


@app.route("/restaurant-dashboard/<int:restaurant_id>/<int:offer_id>/edit", methods=["POST"])
def edit_offer(restaurant_id, offer_id):
    """Edit an offer."""

    restaurant = Restaurant.query.get(restaurant_id)
    offer = Offer.query.get(offer_id)

    item = request.form.get("item")
    quantity = request.form.get("quantity")
    price = request.form.get("price")
    start_time = request.form.get("start-time")
    end_time = request.form.get("end-time")

    offer.item = item
    offer.quantity = quantity
    offer.price = price
    offer.start_time = start_time
    offer.end_time = end_time

    db.session.add(offer)
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
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    connect_to_db(app)
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
