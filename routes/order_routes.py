from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

# Order model
class Order(db.Model, SerializerMixin):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    pickup_address = db.Column(db.Text, nullable=False)
    delivery_address = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='pending')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    def to_dict(self):
        return {
            'order_id': self.order_id,
            'pickup_address': self.pickup_address,
            'delivery_address': self.delivery_address,
            'status': self.status,
            'user_id': self.user_id
        }


class OrderResource(Resource):
    def get(self, order_id=None):
        if order_id:
            order = Order.query.get_or_404(order_id)
            return jsonify(order.to_dict())
        else:
            orders = Order.query.all()
            return jsonify([order.to_dict() for order in orders])

    def post(self):
        data = request.json
        new_order = Order(
            pickup_address=data.get('pickup_address'),
            delivery_address=data.get('delivery_address'),
            user_id=data.get('user_id'),
            status=data.get('status', 'pending')
        )
        db.session.add(new_order)
        db.session.commit()
        return jsonify(new_order.to_dict()), 201

    def put(self, order_id):
        order = Order.query.get_or_404(order_id)
        data = request.json

        order.pickup_address = data.get('pickup_address', order.pickup_address)
        order.delivery_address = data.get('delivery_address', order.delivery_address)
        order.user_id = data.get('user_id', order.user_id)
        order.status = data.get('status', order.status)

        db.session.commit()
        return jsonify(order.to_dict())

    def delete(self, order_id):
        order = Order.query.get_or_404(order_id)
        db.session.delete(order)
        db.session.commit()
        return '', 204

# Add OrderResource to API with endpoint /orders and /orders/<order_id>
api.add_resource(OrderResource, '/orders', '/orders/<int:order_id>')



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
