# app.py
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api
from extensions import db, bcrypt, jwt
from resources import initialize_routes

app = Flask(__name__)

# Configuration (replace with your actual config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'yoursecretkey'

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)
CORS(app)

migrate = Migrate(app, db)
api = Api(app)

initialize_routes(api)

if __name__ == "__main__":
    app.run(debug=True)
