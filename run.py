import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a secure key

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app)
api = Api(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)

# Define parsers for registration and login
register_parser = reqparse.RequestParser()
register_parser.add_argument('username', type=str, required=True, help='Username is required')
register_parser.add_argument('email', type=str, required=True, help='Email is required')
register_parser.add_argument('password', type=str, required=True, help='Password is required')
register_parser.add_argument('phone_number', type=str, required=False)

login_parser = reqparse.RequestParser()
login_parser.add_argument('email', type=str, required=True, help='Email is required')
login_parser.add_argument('password', type=str, required=True, help='Password is required')

# User registration resource
class RegisterResource(Resource):
    def post(self):
        data = register_parser.parse_args()
        username = data['username']
        email = data['email']
        password = data['password']
        phone_number = data.get('phone_number')

        if User.query.filter_by(email=email).first():
            return {'message': 'User with this email already exists'}, 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password, phone_number=phone_number)
        
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User registered successfully'}, 201

# User login resource
class LoginResource(Resource):
    def post(self):
        data = login_parser.parse_args()
        email = data['email']
        password = data['password']

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity={'username': user.username, 'email': user.email})
            return {'access_token': access_token}, 200
        else:
            return {'message': 'Invalid credentials'}, 401

# Add resources to API
api.add_resource(RegisterResource, '/register')
api.add_resource(LoginResource, '/login')

if __name__ == '__main__':
    app.run(debug=True)
