from marshmallow import fields
from app.ext import ma

class RolSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)