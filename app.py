import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse, fields, marshal_with

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

# Define Admin model
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

# Define Food model
class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Food {self.name}>'

# Define Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Product {self.name}>'

# Define Review model
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    review = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# Define parsers for registration and login
register_parser = reqparse.RequestParser()
register_parser.add_argument('username', type=str, required=True, help='Username is required')
register_parser.add_argument('email', type=str, required=True, help='Email is required')
register_parser.add_argument('password', type=str, required=True, help='Password is required')
register_parser.add_argument('phone_number', type=str, required=False)

login_parser = reqparse.RequestParser()
login_parser.add_argument('email', type=str, required=True, help='Email is required')
login_parser.add_argument('password', type=str, required=True, help='Password is required')

food_parser = reqparse.RequestParser()
food_parser.add_argument('name', type=str, required=True, help='Name of the food is required')
food_parser.add_argument('description', type=str, required=True, help='Description of the food is required')
food_parser.add_argument('price', type=float, required=True, help='Price of the food is required')
food_parser.add_argument('image', type=str, required=True, help='Image URL of the food is required')

product_parser = reqparse.RequestParser()
product_parser.add_argument('name', type=str, required=True, help='Name of the product is required')
product_parser.add_argument('description', type=str, required=True, help='Description of the product is required')
product_parser.add_argument('price', type=float, required=True, help='Price of the product is required')
product_parser.add_argument('image', type=str, required=True, help='Image URL of the product is required')

review_parser = reqparse.RequestParser()
review_parser.add_argument('name', type=str, required=True, help='Name is required')
review_parser.add_argument('review', type=str, required=True, help='Review is required')
review_parser.add_argument('rating', type=float, required=True, help='Rating is required')

# Define resource fields
review_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'review': fields.String,
    'rating': fields.Float,
    'created_at': fields.DateTime
}

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

# Admin login resource
class AdminLoginResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        admin = Admin.query.filter_by(email=email).first()
        if admin and admin.check_password(password):
            access_token = create_access_token(identity={'email': admin.email})
            return {'access_token': access_token}, 200
        return {'message': 'Invalid credentials'}, 401

# Food resources
class FoodListResource(Resource):
    def get(self):
        foods = Food.query.all()
        return [{'id': food.id, 'name': food.name, 'description': food.description, 'price': food.price, 'image': food.image} for food in foods]

    def post(self):
        args = food_parser.parse_args()
        food = Food(name=args['name'], description=args['description'], price=args['price'], image=args['image'])
        db.session.add(food)
        db.session.commit()
        return {'id': food.id, 'name': food.name, 'description': food.description, 'price': food.price, 'image': food.image}, 201

class FoodResource(Resource):
    def get(self, food_id):
        food = Food.query.get_or_404(food_id)
        return {'id': food.id, 'name': food.name, 'description': food.description, 'price': food.price, 'image': food.image}

    def put(self, food_id):
        args = food_parser.parse_args()
        food = Food.query.get_or_404(food_id)
        food.name = args['name']
        food.description = args['description']
        food.price = args['price']
        food.image = args['image']
        db.session.commit()
        return {'id': food.id, 'name': food.name, 'description': food.description, 'price': food.price, 'image': food.image}

    def delete(self, food_id):
        food = Food.query.get_or_404(food_id)
        db.session.delete(food)
        db.session.commit()
        return '', 204

# Product resources
class ProductListResource(Resource):
    def get(self):
        products = Product.query.all()
        return [{'id': product.id, 'name': product.name, 'description': product.description, 'price': product.price, 'image': product.image} for product in products]

    def post(self):
        args = product_parser.parse_args()
        product = Product(name=args['name'], description=args['description'], price=args['price'], image=args['image'])
        db.session.add(product)
        db.session.commit()
        return {'id': product.id, 'name': product.name, 'description': product.description, 'price': product.price, 'image': product.image}, 201

class ProductResource(Resource):
    def get(self, product_id):
        product = Product.query.get_or_404(product_id)
        return {'id': product.id, 'name': product.name, 'description': product.description, 'price': product.price, 'image': product.image}

    def put(self, product_id):
        args = product_parser.parse_args()
        product = Product.query.get_or_404(product_id)
        product.name = args['name']
        product.description = args['description']
        product.price = args['price']
        product.image = args['image']
        db.session.commit()
        return {'id': product.id, 'name': product.name, 'description': product.description, 'price': product.price, 'image': product.image}

    def delete(self, product_id):
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return '', 204

# Review resources
class ReviewListResource(Resource):
    @marshal_with(review_fields)
    def get(self):
        reviews = Review.query.all()
        return reviews

    @marshal_with(review_fields)
    def post(self):
        args = review_parser.parse_args()
        review = Review(name=args['name'], review=args['review'], rating=args['rating'])
        db.session.add(review)
        db.session.commit()
        return review, 201

class ReviewResource(Resource):
    @marshal_with(review_fields)
    def get(self, review_id):
        review = Review.query.get_or_404(review_id)
        return review

    def delete(self, review_id):
        review = Review.query.get_or_404(review_id)
        db.session.delete(review)
        db.session.commit()
        return '', 204

# Add resources to API
api.add_resource(RegisterResource, '/register')
api.add_resource(LoginResource, '/login')
api.add_resource(AdminLoginResource, '/admin/login')
api.add_resource(FoodListResource, '/api/foods')
api.add_resource(FoodResource, '/api/foods/<int:food_id>')
api.add_resource(ProductListResource, '/api/products')
api.add_resource(ProductResource, '/api/products/<int:product_id>')
api.add_resource(ReviewListResource, '/api/reviews')
api.add_resource(ReviewResource, '/api/reviews/<int:review_id>')

if __name__ == '__main__':
    app.run(debug=True)
