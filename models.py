# models.py
from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {"id": self.id, "username": self.username, "email": self.email}

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email, "phone": self.phone}

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    discounted_price = db.Column(db.Float, nullable=True)
    img = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": self.price, "discounted_price": self.discounted_price, "img": self.img}

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    review = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "review": self.review, "rating": self.rating}
