from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

# Define User model with SQLAlchemy
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(110), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    role = db.Column(db.String(50), nullable=False)

def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
            'role': self.role
        }

# RESTful Resource for User operations
class UserResource(Resource):
    def get(self, id=None):
        if id:
            user = User.query.get_or_404(id)
            return jsonify(user.to_dict())
        else:
            users = User.query.all()
            return jsonify([user.to_dict() for user in users])

    def post(self):
        data = request.json
        new_user = User(
            username=data.get('username'),
            email=data.get('email'),
            password=data.get('password'),
            role=data.get('role')
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201

    def put(self, id):
        user = User.query.get_or_404(id)
        data = request.json

        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.password = data.get('password', user.password)
        user.role = data.get('role', user.role)

        db.session.commit()
        return jsonify(user.to_dict())

    def delete(self, id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

# Add the UserResource to the API with endpoint /users/<int:id>
api.add_resource(UserResource, '/users', '/users/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
