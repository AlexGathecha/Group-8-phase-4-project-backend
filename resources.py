# resources.py
from sqlite3 import IntegrityError
from flask_restful import Resource
from flask import request, jsonify
from extensions import db, bcrypt
from models import User, Contact, MenuItem, Review
from flask_jwt_extended import create_access_token

class RegisterApi(Resource):
    def post(self):
        data = request.get_json()
        if not data or not 'username' in data or not 'email' in data or not 'password' in data:
            return jsonify({"message": "Missing required fields"}), 400
        try:
            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            new_user = User(username=data['username'], email=data['email'], password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message": "User registered successfully"}), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({"message": "User already exists"}), 409
        except Exception as e:
            return jsonify({"message": str(e)}), 500

class LoginApi(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user and bcrypt.check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity={'username': user.username, 'email': user.email})
            return jsonify(access_token=access_token)
        return jsonify({"message": "Invalid credentials"})

class ContactApi(Resource):
    def get(self):
        contacts = Contact.query.all()
        return jsonify([contact.to_dict() for contact in contacts])

    def post(self):
        data = request.get_json()
        new_contact = Contact(name=data['name'], email=data['email'], phone=data['phone'])
        db.session.add(new_contact)
        db.session.commit()
        return jsonify({"message": "Contact added successfully"})

class MenuApi(Resource):
    def get(self):
        menu_items = MenuItem.query.all()
        return jsonify([item.to_dict() for item in menu_items])

    def post(self):
        data = request.get_json()
        new_item = MenuItem(name=data['name'], price=data['price'], discounted_price=data.get('discounted_price'), img=data['img'])
        db.session.add(new_item)
        db.session.commit()
        return jsonify({"message": "Menu item added successfully"})

class ReviewApi(Resource):
    def get(self):
        reviews = Review.query.all()
        return jsonify([review.to_dict() for review in reviews])

    def post(self):
        data = request.get_json()
        new_review = Review(name=data['name'], review=data['review'], rating=data['rating'])
        db.session.add(new_review)
        db.session.commit()
        return jsonify({"message": "Review added successfully"})

def initialize_routes(api):
    api.add_resource(RegisterApi, '/api/register')
    api.add_resource(LoginApi, '/api/login')
    api.add_resource(ContactApi, '/api/contacts')
    api.add_resource(MenuApi, '/api/menu')
    api.add_resource(ReviewApi, '/api/reviews')
