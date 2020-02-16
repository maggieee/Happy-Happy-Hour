from model import connect_to_db, db, Restaurant, Offer
from server import app


def kaboom():

  print("Kaboom")

  Offer.query.delete()
  Restaurant.query.delete()


def load_restaurants():
    """Load restaurants from restaurants.txt into database."""

    print("Restaurants")

    # Read restaurants.txt file and insert data
    for row in open("seed_data/restaurants.txt"):
        row = row.rstrip()
        name, street_address, city, state, zipcode, email, password = row.split("|")

        restaurant = Restaurant(name=name,
                     street_address=street_address,
                     city=city,
                     state=state,
                     zipcode=zipcode,
                     email=email)
        
        restaurant.set_password(password)


        # We need to add to the session or it won't ever be stored
        db.session.add(restaurant)

    # Once we're done, we should commit our work
    db.session.commit()


# def load_offers():
#     """Load posts from offers.txt into database."""

#     print("Offers")

#     # Read offers.txt file and insert data
#     for row in open("seed_data/offers.txt"):
#         row = row.rstrip()
#         restaurant_id, item = row.split("|")

#         offer = Offer(restaurant_id=restaurant_id,
#                       item=item)

#         # We need to add to the session or it won't ever be stored
#         db.session.add(offer)

#     # Once we're done, we should commit our work
#     db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # kaboom()
    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_restaurants()
    # load_offers()
