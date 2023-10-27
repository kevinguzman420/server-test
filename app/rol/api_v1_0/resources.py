from flask import request, jsonify
from flask_restful import Api, Resource

# blueprints
from . import rol_bp

# models
from app.rol.models import Rol

# schemas
from .schemas import RolSchema

api = Api(rol_bp)

# roles
class RolResource(Resource):
    def get(self):
        roles = Rol.get_all()
        return jsonify(RolSchema(many=True).dump(roles))
        
    def post(self):
        rol = Rol(**request.json)
        rol.save()
        return jsonify(message="Rol created successfully", status_code=201)

api.add_resource(RolResource, '/rol', endpoint="rol")

class RolGetOne(Resource):
    def get(self, id):
        rol = Rol.get_by_id(id)
        rol = RolSchema().dump(rol)
        return jsonify(rol)
    
    def delete(self, id):
        rol = Rol.get_by_id(id)
        rol.delete()
        return jsonify(message="Rol deleted successfully", status_code=200)

api.add_resource(RolGetOne, '/rol/<int:id>', endpoint="rol_get_one")
