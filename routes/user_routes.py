from flask_restful import Resource
from config import db
from models import User

class UserResource(Resource):
    def get(self, id=None):
        if id:
            user = User.query.get(id)
            return user.to_dict()
        users = User.query.all()
        return [user.to_dict() for user in users]

    def post(self):
        
        pass

    def put(self, id):
        # Handle user update
        pass

    def delete(self, id):
        # Handle user deletion
        pass
