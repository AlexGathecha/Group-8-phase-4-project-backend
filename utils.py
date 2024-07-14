from app import db
from models import User, Contact, MenuItem, Review

def init_db():
    db.create_all()
    print("Database initialized")

def clear_db():
    db.drop_all()
    print("Database cleared")
