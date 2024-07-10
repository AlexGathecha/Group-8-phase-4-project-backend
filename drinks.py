from flask import Blueprint
from flask_restful import Api, Resource, reqparse

drink_bp = Blueprint('drink_bp', __name__, url_prefix='/drinks')
api_bp = Api(drink_bp)

drink_parser = reqparse.RequestParser()
drink_parser.add_argument('name', type=str, required=True, help='Name of the drink is required')
drink_parser.add_argument('type', type=str, required=True, help='Type of the drink is required')
drink_parser.add_argument('price', type=float, required=True, help='Price of the drink is required')


class Drink(Resource):
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


api_bp.add_resource(Drink, '/<int:id>')


class DrinkList(Resource):
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


api_bp.add_resource(DrinkList, '/all')
