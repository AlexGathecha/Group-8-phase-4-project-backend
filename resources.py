import logging
from flask_restful import Resource
from flask import jsonify, request
from extensions import db, bcrypt
from models import User, Contact, MenuItem, Review
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import JWTManager

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class RegisterApi(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        logging.debug(f"Register attempt for email: {email}")

        if not username or not email or not password:
            return {"message": "Missing required fields"}, 400

        try:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(username=username, email=email.lower(), password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return {"message": "User registered successfully"}, 201
        except IntegrityError:
            db.session.rollback()
            return {"message": "User already exists"}, 409
        except Exception as e:
            logging.error(f"Exception: {str(e)}")
            return {"message": str(e)}, 500

class LoginApi(Resource):
    def post(self):
        try:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')

            logging.debug(f"Login attempt for email: {email}")

            if not email or not password:
                return {"message": "Missing email or password"}, 400

            user = User.query.filter_by(email=email).first()
            if user and bcrypt.check_password_hash(user.password, password):
                access_token = create_access_token(identity={'username': user.username, 'email': user.email})
                logging.debug(f"Access token created for email: {email}")
                return {"access_token": access_token}, 200

            logging.debug("Invalid credentials")
            return {"message": "Invalid credentials"}, 401

        except Exception as e:
            logging.error(f"Exception: {str(e)}")
            return {"message": str(e)}, 500

class ContactApi(Resource):
    def get(self):
        contacts = Contact.query.all()
        return [contact.to_dict() for contact in contacts]

    def post(self):
        data = request.get_json()
        new_contact = Contact(name=data['name'], email=data['email'], phone=data['phone'])
        db.session.add(new_contact)
        db.session.commit()
        return {"message": "Contact added successfully"}

class MenuApi(Resource):
    def get(self):
        menu_items = MenuItem.query.all()
        return [item.to_dict() for item in menu_items]

    def post(self):
        data = request.get_json()
        new_item = MenuItem(name=data['name'], price=data['price'], discounted_price=data.get('discounted_price'), img=data['img'])
        db.session.add(new_item)
        db.session.commit()
        return {"message": "Menu item added successfully"}

class ReviewApi(Resource):
    def get(self):
        reviews = Review.query.all()
        return [review.to_dict() for review in reviews]

    def post(self):
        data = request.get_json()
        new_review = Review(name=data['name'], review=data['review'], rating=data['rating'])
        db.session.add(new_review)
        db.session.commit()
        return {"message": "Review added successfully"}
class CheckLoginStatusApi(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return {"logged_in_as": current_user}, 200

def initialize_routes(api):
    api.add_resource(RegisterApi, '/api/register')
    api.add_resource(LoginApi, '/api/login')
    api.add_resource(ContactApi, '/api/contacts')
    api.add_resource(MenuApi, '/api/menu')
    api.add_resource(ReviewApi, '/api/reviews')
    api.add_resource(CheckLoginStatusApi, '/api/checkLoginStatus')
