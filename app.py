
from flask import Flask
from config import db
from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource

from database import db
from models import User, Order, Item, Feedback

# Initialize the flask application
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

from routes import user_routes, order_routes, item_routes, feedback_routes
api = Api(app)

@app.route('/')
def index():
    return "<h1>Welcome to the Parcel Pro App</h1>"

class Users(Resource):
    def get(self):
        users = User.query.all()
        users_list = [user.to_dict() for user in users]
        return make_response(jsonify({"count": len(users_list), "users": users_list}), 200)

    def post(self):
        new_user = User(
            username=request.json.get("username"),
            email=request.json.get("email"),
            password=request.json.get("password"),
            role=request.json.get("role")
        )
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify(new_user.to_dict()), 201)

api.add_resource(Users, '/users')

class UserByID(Resource):
    def get(self, id):
        user = User.query.get(id)
        if user is None:
            return make_response(jsonify({"message": "User not found"}), 404)
        return make_response(jsonify(user.to_dict()), 200)

    def patch(self, id):
        user = User.query.get(id)
        if user is None:
            return make_response(jsonify({"message": "User not found"}), 404)
        for attr in request.json:
            setattr(user, attr, request.json.get(attr))
        db.session.commit()
        return make_response(jsonify(user.to_dict()), 200)

    def delete(self, id):
        user = User.query.get(id)
        if user is None:
            return make_response(jsonify({"message": "User not found"}), 404)
        db.session.delete(user)
        db.session.commit()
        return make_response(jsonify({"message": "User deleted"}), 200)

api.add_resource(UserByID, '/users/<int:id>')

class Orders(Resource):
    def get(self):
        orders = Order.query.all()
        orders_list = [order.to_dict() for order in orders]
        return make_response(jsonify({"count": len(orders_list), "orders": orders_list}), 200)

    def post(self):
        new_order = Order(
            pickup_address=request.json.get("pickup_address"),
            delivery_address=request.json.get("delivery_address"),
            status=request.json.get("status"),
            user_id=request.json.get("user_id")
        )
        db.session.add(new_order)
        db.session.commit()
        return make_response(jsonify(new_order.to_dict()), 201)

api.add_resource(Orders, '/orders')

class OrderByID(Resource):
    def get(self, id):
        order = Order.query.get(id)
        if order is None:
            return make_response(jsonify({"message": "Order not found"}), 404)
        return make_response(jsonify(order.to_dict()), 200)

    def patch(self, id):
        order = Order.query.get(id)
        if order is None:
            return make_response(jsonify({"message": "Order not found"}), 404)
        for attr in request.json:
            setattr(order, attr, request.json.get(attr))
        db.session.commit()
        return make_response(jsonify(order.to_dict()), 200)

    def delete(self, id):
        order = Order.query.get(id)
        if order is None:
            return make_response(jsonify({"message": "Order not found"}), 404)
        db.session.delete(order)
        db.session.commit()
        return make_response(jsonify({"message": "Order deleted"}), 200)

api.add_resource(OrderByID, '/orders/<int:id>')

class Items(Resource):
    def get(self):
        items = Item.query.all()
        items_list = [item.to_dict() for item in items]
        return make_response(jsonify({"count": len(items_list), "items": items_list}), 200)

    def post(self):
        new_item = Item(
            item_name=request.json.get("item_name"),
            description=request.json.get("description"),
            price=request.json.get("price"),
            order_id=request.json.get("order_id")
        )
        db.session.add(new_item)
        db.session.commit()
        return make_response(jsonify(new_item.to_dict()), 201)

api.add_resource(Items, '/items')

class ItemByID(Resource):
    def get(self, id):
        item = Item.query.get(id)
        if item is None:
            return make_response(jsonify({"message": "Item not found"}), 404)
        return make_response(jsonify(item.to_dict()), 200)

    def patch(self, id):
        item = Item.query.get(id)
        if item is None:
            return make_response(jsonify({"message": "Item not found"}), 404)
        for attr in request.json:
            setattr(item, attr, request.json.get(attr))
        db.session.commit()
        return make_response(jsonify(item.to_dict()), 200)

    def delete(self, id):
        item = Item.query.get(id)
        if item is None:
            return make_response(jsonify({"message": "Item not found"}), 404)
        db.session.delete(item)
        db.session.commit()
        return make_response(jsonify({"message": "Item deleted"}), 200)

api.add_resource(ItemByID, '/items/<int:id>')

class Feedbacks(Resource):
    def get(self):
        feedbacks = Feedback.query.all()
        feedbacks_list = [feedback.to_dict() for feedback in feedbacks]
        return make_response(jsonify({"count": len(feedbacks_list), "feedbacks": feedbacks_list}), 200)

    def post(self):
        new_feedback = Feedback(
            rating=request.json.get("rating"),
            comment=request.json.get("comment"),
            order_id=request.json.get("order_id")
        )
        db.session.add(new_feedback)
        db.session.commit()
        return make_response(jsonify(new_feedback.to_dict()), 201)

api.add_resource(Feedbacks, '/feedbacks')

class FeedbackByID(Resource):
    def get(self, id):
        feedback = Feedback.query.get(id)
        if feedback is None:
            return make_response(jsonify({"message": "Feedback not found"}), 404)
        return make_response(jsonify(feedback.to_dict()), 200)

    def patch(self, id):
        feedback = Feedback.query.get(id)
        if feedback is None:
            return make_response(jsonify({"message": "Feedback not found"}), 404)
        for attr in request.json:
            setattr(feedback, attr, request.json.get(attr))
        db.session.commit()
        return make_response(jsonify(feedback.to_dict()), 200)

    def delete(self, id):
        feedback = Feedback.query.get(id)
        if feedback is None:
            return make_response(jsonify({"message": "Feedback not found"}), 404)
        db.session.delete(feedback)
        db.session.commit()
        return make_response(jsonify({"message": "Feedback deleted"}), 200)

api.add_resource(FeedbackByID, '/feedbacks/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
if __name__ == "__main__":
    app.run(port=5555, debug=True)