"""Utility file to seed brightbook database/"""

from sqlalchemy import func
from model import Restaurant
from model import Offer

from model import connect_to_db, db
from server import app

from datetime import datetime


def kaboom():
    """Clear out User, Post, and Heart tables"""

    print("Kaboom")

    Restaurant.query.delete()
    Offer.query.delete()


def load_restaurants():
    """Load restaurants from restaurants.txt into database."""

    print("Restaurants")

    # Read restaurants.txt file and insert data
    for row in open("seed_data/restaurants.txt"):
        row = row.rstrip()
        name, street_address, city, state, zip, email, password = row.split("|")

        restaurant = Restaurant(name=name,
                    street_address=street_address,
                    city=city,
                    state=state,
                    zip=zip,
                    email=email,
                    password=password)
        restaurant.set_password('password')

        # We need to add to the session or it won't ever be stored
        db.session.add(restaurant)

    # Once we're done, we should commit our work
    db.session.commit()


def load_offers():
    """Load posts from offers.txt into database."""

    print("Offers")

    # Read offers.txt file and insert data
    for row in open("seed_data/offers.txt"):
        row = row.rstrip()
        restaurant_id, start_time, end_time, item_name, quantity, price = row.split("|")

        offer = Offer(restaurant_id=restaurant_id,
                    start_time=start_time,
                    end_time=end_time,
                    item_name=item_name,
                    quantity=quantity,
                    price=price)

        # We need to add to the session or it won't ever be stored
        db.session.add(offer)

    # Once we're done, we should commit our work
    db.session.commit()


def set_val_restaurant_id():
    """Set value for the next restaurant id after seeding database"""

    # Get the Max restaurant id in the database
    result = db.session.query(func.max(Restaurant.id)).one()
    max_id = int(result[0])

    # Set the value for the next restaurant id to be max_id + 1
    query = "SELECT setval('restaurants_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()

def set_val_offer_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(Offer.id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('offers_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    kaboom()
    # Import different types of data
    load_restaurants()
    load_offers()
    set_val_restaurant_id()
    set_val_offer_id()
