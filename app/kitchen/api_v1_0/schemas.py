from marshmallow import fields

from app.ext import ma

class MenuSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    description = fields.String()
    price = fields.Float()
    image = fields.String()

class ExtrasCategorySchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()

class ExtrasSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    price = fields.Float()
    extras_category_id = fields.Integer()

class OrderByCustomerSchema(ma.Schema):
    total = fields.Float()
    date = fields.Date()
    status_order_id = fields.Integer()
    quantity = fields.Integer()
    subtotal = fields.Float()
    image = fields.String()
    price = fields.Float()
    name = fields.String()
    