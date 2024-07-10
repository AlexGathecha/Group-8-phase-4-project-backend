from flask import Blueprint
from flask_restful import Api, Resource, reqparse

cake_bp = Blueprint('cake_bp', __name__, url_prefix='/cakes')
api_bp = Api(cake_bp)

cake_parser = reqparse.RequestParser()
cake_parser.add_argument('name', type=str, required=True, help='Name of the cake is required')
cake_parser.add_argument('type', type=str, required=True, help='Type of the cake is required')
cake_parser.add_argument('price', type=float, required=True, help='Price of the cake is required')


class Cake(Resource):
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


api_bp.add_resource(Cake, '/<int:id>')


class CakeList(Resource):
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


api_bp.add_resource(CakeList, '/all')
