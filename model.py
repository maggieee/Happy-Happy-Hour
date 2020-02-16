from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc

db = SQLAlchemy()


class Restaurant(db.Model):
    """A restaurant user."""

    __tablename__ = "restaurants"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    street_address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(40), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zipcode = db.Column(db.String(11), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    offers = db.relationship("Offer", backref=db.backref("restaurant"))

    def __repr__(self):

        return f"<Restaurant id={self.id}, name={self.name}>"


class Offer(db.Model):
    """An offer created by a restaurant."""

    __tablename__ = "offers"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    restaurant_id = db.Column(db.Integer, 
                           db.ForeignKey("restaurants.id"))
    item = db.Column(db.Text, nullable=False)

    def __repr__(self):

        return f"<Offer id={self.id}, restaurant={self.restaurant_id} item={self.item}>"



def connect_to_db(app):
    """Connect Flask app to database."""

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql:///happyhappy'
    app.config["SQLALCHEMY_ECHO"] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    