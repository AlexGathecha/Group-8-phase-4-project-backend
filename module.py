from flask import Blueprint, Flask
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # Example database URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    return app

def create_cake_module(app):
    from models import Cake  # Import Cake model from models.py

    cake_bp = Blueprint('cake_bp', __name__, url_prefix='/cakes')
    api_bp = Api(cake_bp)

    cake_parser = reqparse.RequestParser()
    cake_parser.add_argument('name', type=str, required=True, help='Name of the cake is required')
    cake_parser.add_argument('type', type=str, required=True, help='Type of the cake is required')
    cake_parser.add_argument('price', type=float, required=True, help='Price of the cake is required')

    class CakeResource(Resource):
        def get(self, id):
            cake = Cake.query.get_or_404(id)
            return {'id': cake.id, 'name': cake.name, 'type': cake.type, 'price': cake.price}

        def put(self, id):
            data = cake_parser.parse_args()
            cake = Cake.query.get_or_404(id)
            cake.name = data['name']
            cake.type = data['type']
            cake.price = data['price']
            db.session.commit()
            return {'id': cake.id, 'name': cake.name, 'type': cake.type, 'price': cake.price}

        def delete(self, id):
            cake = Cake.query.get_or_404(id)
            db.session.delete(cake)
            db.session.commit()
            return {'message': 'Cake deleted successfully'}

    api_bp.add_resource(CakeResource, '/<int:id>')

    class CakeListResource(Resource):
        def get(self):
            cakes = Cake.query.all()
            return [{'id': c.id, 'name': c.name, 'type': c.type, 'price': c.price} for c in cakes]

        def post(self):
            data = cake_parser.parse_args()
            new_cake = Cake(name=data['name'], type=data['type'], price=data['price'])
            db.session.add(new_cake)
            db.session.commit()
            return {'message': 'Cake created successfully'}

        def delete(self, id):
            cake = Cake.query.get_or_404(id)
            db.session.delete(cake)
            db.session.commit()
            return {'message': 'Cake deleted successfully'}

    api_bp.add_resource(CakeListResource, '/all')

    return cake_bp

def create_drink_module(app):
    from models import Drink  # Import Drink model from models.py

    drink_bp = Blueprint('drink_bp', __name__, url_prefix='/drinks')
    api_bp = Api(drink_bp)

    drink_parser = reqparse.RequestParser()
    drink_parser.add_argument('name', type=str, required=True, help='Name of the drink is required')
    drink_parser.add_argument('type', type=str, required=True, help='Type of the drink is required')
    drink_parser.add_argument('price', type=float, required=True, help='Price of the drink is required')

    class DrinkResource(Resource):
        def get(self, id):
            drink = Drink.query.get_or_404(id)
            return {'id': drink.id, 'name': drink.name, 'type': drink.type, 'price': drink.price}

        def put(self, id):
            data = drink_parser.parse_args()
            drink = Drink.query.get_or_404(id)
            drink.name = data['name']
            drink.type = data['type']
            drink.price = data['price']
            db.session.commit()
            return {'id': drink.id, 'name': drink.name, 'type': drink.type, 'price': drink.price}

        def delete(self, id):
            drink = Drink.query.get_or_404(id)
            db.session.delete(drink)
            db.session.commit()
            return {'message': 'Drink deleted successfully'}

    api_bp.add_resource(DrinkResource, '/<int:id>')

    class DrinkListResource(Resource):
        def get(self):
            drinks = Drink.query.all()
            return [{'id': d.id, 'name': d.name, 'type': d.type, 'price': d.price} for d in drinks]

        def post(self):
            data = drink_parser.parse_args()
            new_drink = Drink(name=data['name'], type=data['type'], price=data['price'])
            db.session.add(new_drink)
            db.session.commit()
            return {'message': 'Drink created successfully'}

        def delete(self, id):
            drink = Drink.query.get_or_404(id)
            db.session.delete(drink)
            db.session.commit()
            return {'message': 'Drink deleted successfully'}

    api_bp.add_resource(DrinkListResource, '/all')

    return drink_bp

def create_ice_cream_module(app):
    from models import IceCream  # Import IceCream model from models.py

    ice_cream_bp = Blueprint('ice_cream_bp', __name__, url_prefix='/ice_creams')
    api_bp = Api(ice_cream_bp)

    ice_cream_parser = reqparse.RequestParser()
    ice_cream_parser.add_argument('name', type=str, required=True, help='Name of the ice cream is required')
    ice_cream_parser.add_argument('flavor', type=str, required=True, help='Flavor of the ice cream is required')
    ice_cream_parser.add_argument('price', type=float, required=True, help='Price of the ice cream is required')

    class IceCreamResource(Resource):
        def get(self, id):
            ice_cream = IceCream.query.get_or_404(id)
            return {'id': ice_cream.id, 'name': ice_cream.name, 'flavor': ice_cream.flavor, 'price': ice_cream.price}

        def put(self, id):
            data = ice_cream_parser.parse_args()
            ice_cream = IceCream.query.get_or_404(id)
            ice_cream.name = data['name']
            ice_cream.flavor = data['flavor']
            ice_cream.price = data['price']
            db.session.commit()
            return {'id': ice_cream.id, 'name': ice_cream.name, 'flavor': ice_cream.flavor, 'price': ice_cream.price}

        def delete(self, id):
            ice_cream = IceCream.query.get_or_404(id)
            db.session.delete(ice_cream)
            db.session.commit()
            return {'message': 'Ice cream deleted successfully'}

    api_bp.add_resource(IceCreamResource, '/<int:id>')

    class IceCreamListResource(Resource):
        def get(self):
            ice_creams = IceCream.query.all()
            return [{'id': ic.id, 'name': ic.name, 'flavor': ic.flavor, 'price': ic.price} for ic in ice_creams]

        def post(self):
            data = ice_cream_parser.parse_args()
            new_ice_cream = IceCream(name=data['name'], flavor=data['flavor'], price=data['price'])
            db.session.add(new_ice_cream)
            db.session.commit()
            return {'message': 'Ice cream created successfully'}

        def delete(self, id):
            ice_cream = IceCream.query.get_or_404(id)
            db.session.delete(ice_cream)
            db.session.commit()
            return {'message': 'Ice cream deleted successfully'}

    api_bp.add_resource(IceCreamListResource, '/all')

    return ice_cream_bp
