from flask import request, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import jwt_required
# from flask_jwt_extended import current_user
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import set_refresh_cookies
from flask_jwt_extended import unset_jwt_cookies
from flask_jwt_extended import get_jwt
from datetime import timedelta

# blueprints
from . import users_bp

# models
from app.users.models import Users
from app.rol.models import Rol

# schemas
from .schemas import UsersSchema

# misc
from app.db import db
from app import jwt

api = Api(users_bp)

# users


class UsersSignupResource(Resource):
    def get(self):
        users = Users.query.join(Rol).filter(Users.rol_id == Rol.id).add_columns(
            Users.id, Users.username, Users.email, Rol.name).all()
        users = UsersSchema(many=True).dump(users)
        return jsonify(users=users, status_code=200)

    def post(self):
        user = Users(**request.json)  # username, email, password
        user.generate_password(request.json['password'])
        user.rol_id = request.json.get("rol_id", 1)  # 1 -> customer id
        user.save()
        return jsonify(message="User created successfully", status_code=201)


api.add_resource(UsersSignupResource, '/users/signup', endpoint="users_signup")


class UsersSigninResource(Resource):
    def post(self):
        user = Users.get_by_email(request.json["email"])
        if user is not None and user.check_password(request.json["password"]):
            access_token = create_access_token(identity=user)
            refresh_token = create_refresh_token(identity=user)
            # print(access_token)
            response = jsonify(message="login successful",
                               access_token=access_token,
                               refresh_token=refresh_token,
                               status_code=200)
            # set_access_cookies(response, access_token)
            # set_refresh_cookies(response, refresh_token)
            # response.headers['Access-Control-Allow-Credentials'] = "true"
            return response
        return jsonify(message="User doesn't exits", status_code=401)


api.add_resource(UsersSigninResource, "/users/signin", endpoint="users_signin")


class UserGetOneResource(Resource):
    def get(self, userId):
        user = Users.get_by_id(userId)
        user = UsersSchema().dump(user)
        return jsonify(user=user, status_code=200)


api.add_resource(UserGetOneResource, '/users/<int:userId>',
                 endpoint="user_get_one")


class UsersChangeRolResource(Resource):
    def put(self, userId):
        user = Users.get_by_id(userId)
        user.rol_id = request.json["rol_id"]
        user.save()
        return jsonify(message="User's rol updated", status_code=200)


api.add_resource(UsersChangeRolResource,
                 '/users/change-rol/<int:userId>', endpoint="users_change_rol")


class UsersRefreshToken(Resource):

    @jwt_required(refresh=True)
    def post(self):
        # token = request.json["token"]
        current_user = get_jwt_identity()
        print(current_user)
        new_access_token = create_access_token(identity=current_user)
        return jsonify(access_token=new_access_token), 200


api.add_resource(UsersRefreshToken, "/users/refresh-token",
                 endpoint="user_refresh_token")


class UsersTokenValidateResource(Resource):
    @jwt_required()
    def post(self):
        # token = request.json["token"]

        try:
            token_info = get_jwt()
            # Obtén la información del token

            # Verifica si el token ha expirado
            if token_info['exp'] < time.time():
                return jsonify(message="Token expirado"), 401
            return jsonify(message="Success", status_code=200)

            # claims = jwt.decode(token)
            # return jsonify(message="Success", status_code=200)
        except:
            return jsonify(message="Expired token", status_code=401)


api.add_resource(UsersTokenValidateResource,
                 "/users/token-validate", endpoint="users_token_validate")


# class TestResource(Resource):
#     # @jwt_required()
#     def get(self):
#         return jsonify(
#             id=current_user.id,
#             full_name=current_user.email,
#             password=current_user.password,
#             username=current_user.username,
#         )


# api.add_resource(TestResource, "/test", endpoint="test")


@jwt.user_identity_loader
def user_identity_loopup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return Users.get_by_id(identity)
