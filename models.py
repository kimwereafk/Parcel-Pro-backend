from config import db
from sqlalchemy_serializer import SerializerMixin

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(110), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    orders = db.relationship('Order', backref='user', lazy=True)

class Order(db.Model, SerializerMixin):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    pickup_address = db.Column(db.Text, nullable=False)
    delivery_address = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='pending')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    items = db.relationship('Item', backref='order', lazy=True)
    feedback = db.relationship('Feedback', backref='order', lazy=True)

class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)

class Feedback(db.Model, SerializerMixin):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)

class OrderItem(db.Model, SerializerMixin):
    __tablename__ = 'order_item'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), primary_key=True)
