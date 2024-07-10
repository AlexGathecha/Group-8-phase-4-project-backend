from flask import Blueprint
from flask_restful import Api, Resource, reqparse

ice_cream_bp = Blueprint('ice_cream_bp', __name__, url_prefix='/ice_creams')
api_bp = Api(ice_cream_bp)

ice_cream_parser = reqparse.RequestParser()
ice_cream_parser.add_argument('name', type=str, required=True, help='Name of the ice cream is required')
ice_cream_parser.add_argument('flavor', type=str, required=True, help='Flavor of the ice cream is required')
ice_cream_parser.add_argument('price', type=float, required=True, help='Price of the ice cream is required')


class IceCream(Resource):
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


api_bp.add_resource(IceCream, '/<int:id>')


class IceCreamList(Resource):
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


api_bp.add_resource(IceCreamList, '/all')
