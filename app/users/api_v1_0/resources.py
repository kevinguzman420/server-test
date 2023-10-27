from flask import request, jsonify
from flask_restful import Api, Resource

# blueprints
from . import users_bp

# models
from app.users.models import Users
from app.rol.models import Rol

# schemas
from .schemas import UsersSchema

# misc
from app.db import db

api = Api(users_bp)

# users
class UsersResource(Resource):
    def get(self):
        users = Users.query.join(Rol).filter(Users.rol_id == Rol.id).add_columns(Users.id, Users.username, Users.email, Rol.name).all()
        users = UsersSchema(many=True).dump(users)
        return jsonify(users=users, status_code=200)

    def post(self):
        user = Users(**request.json) # username, email, password
        user.generate_password(request.json['password'])
        user.save()
        return jsonify(message="User created successfully", status_code=201)

api.add_resource(UsersResource, '/users', endpoint="users")

class UserGetOneResource(Resource):
    def get(self, userId):
        user = Users.get_by_id(userId)
        user = UsersSchema().dump(user)
        return jsonify(user=user, status_code=200)

api.add_resource(UserGetOneResource, '/users/<int:userId>', endpoint="user_get_one")

class UsersChangeRolResource(Resource):
    def put(self, userId):
        user = Users.get_by_id(userId)
        user.rol_id = request.json["rol_id"]
        user.save()
        return jsonify(message="User's rol updated", status_code=200)

api.add_resource(UsersChangeRolResource, '/users/change-rol/<int:userId>', endpoint="users_change_rol")