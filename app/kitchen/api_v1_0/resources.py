from flask import request, jsonify, current_app
from flask_restful import Api, Resource
from flask_socketio import emit
from flask_jwt_extended import jwt_required
from datetime import date
import logging
import sqlalchemy
import json


# blueprints
from . import kitchen_bp

# models
from app.users.models import Users
from app.kitchen.models import Order, OrderMenu, Menu, ExtrasCategory, Extras, OrderMenuExtras, StatusOrder

# schemas
from app.kitchen.api_v1_0.schemas import MenuSchema, ExtrasCategorySchema, ExtrasSchema, OrderByCustomerSchema

# misc
from app import socketio

logger = logging.getLogger(__name__)
api = Api(kitchen_bp)

# status order | postman | user


class KitchenStatusOrderResource(Resource):
    def post(self):
        status_order = StatusOrder(**request.json)
        status_order.save()
        return jsonify(message="Status order created successfully", status_code=201)


api.add_resource(KitchenStatusOrderResource,
                 "/kitchen/status-order", endpoint="status_order")

# extras-category | postman


class KitchenExtrasCategoryResource(Resource):
    # ✔
    def get(self):
        extras_category = ExtrasCategory.get_all()
        extras_category = ExtrasCategorySchema(many=True).dump(extras_category)
        return jsonify(extras_category=extras_category, status_code=200)

    # ✔
    def post(self):
        try:
            extraCategory = ExtrasCategory(**request.json)
            extraCategory.save()
            # logger.info("Extra category created successfully")
            return jsonify(message="Extra category created successfully", status_code=201)
        except:
            logger.error("There's an error trying to create a Extra Category")
            return jsonify(message="There's an error trying to create a Extra Category", status_code=500)


api.add_resource(KitchenExtrasCategoryResource,
                 "/kitchen/extras-category", endpoint="kitchen_extras_category")

# extras | postman


class KitchenExtrasResource(Resource):
    # ✔
    def get(self):
        extras = Extras.get_all()
        extras = ExtrasSchema(many=True).dump(extras)
        return jsonify(extras=extras)
    # ✔

    def post(self):
        try:
            extra = Extras(**request.json)
            extra.save()
            return jsonify(message="Extra created successfully", status_code=201)
        except Exception as e:
            logger.error("There's an error trying to create the Extra.")
            logger.error(e)
            return jsonify(message="There's an error trying to create the Extra.", status_code=500)


api.add_resource(KitchenExtrasResource, "/kitchen/extras",
                 endpoint="kitchen_extras")

# extras by category


class KitchenExtrasByExtrasCategoryResource(Resource):
    def get(self, extraCategoryId):
        extras = Extras.query.filter_by(extras_category_id=extraCategoryId)
        extras = ExtrasSchema().dump(extras, many=True)
        return jsonify(extras=extras, status_code=200)


api.add_resource(KitchenExtrasByExtrasCategoryResource,
                 "/kitchen/extras/extras-category/<int:extraCategoryId>", endpoint="get_extras_by_extras_category_id")

# menu | postman


class KitchenMenuResource(Resource):
    @jwt_required()
    def get(self):
        menus = Menu.get_all()
        menus = MenuSchema(many=True).dump(menus)
        return jsonify(menus=menus, status_code=200)

    def post(self):
        menu = Menu(**request.json)
        menu.save()
        return jsonify(message="Menu created successfully", status_code=201)


api.add_resource(KitchenMenuResource, "/kitchen/menu", endpoint="kitchen_menu")

# orders | customer


class KitchenOrdersResource(Resource):
    @jwt_required()
    def post(self):
        # save the order
        total = 0
        for order in request.json:
            total += order["subtotal"]

        new_order = Order(total=total,
                          date=date.today(),
                          status_order_id=1,  # 1: status by default
                          client_id=1)  # 1: change it later
        new_order.save()

        # orders menu
        for order in request.json:
            order_menu = OrderMenu(
                quantity=order["quantity"],
                subtotal=order["subtotal"],
                menu_id=order["menu"]["id"],
                order_id=new_order.id
            )
            order_menu.save()

            # order extras
            for extra in order["extras"]:
                order_menu_extra = OrderMenuExtras(
                    order_id=order_menu.id,
                    extra_id=extra["id"],
                )
                order_menu_extra.save()

        return jsonify(message="Order created successfully", status_code=201)


api.add_resource(KitchenOrdersResource, '/kitchen/orders',
                 endpoint="kitchen_orders")


# get order by customer | customer
class KitchenOrdersByCustomerResource(Resource):
    @jwt_required()
    def get(self, clientId):
        results = Order.query.filter_by(client_id=clientId).all()
        orders = objetIntoJson(results)
        return jsonify(orders=orders)


api.add_resource(KitchenOrdersByCustomerResource,
                 "/kitchen/orders-by-customer/<int:clientId>", endpoint="orders_by_customer")

# update status order | user


class KitchenOrdersUpdateOrderResource(Resource):
    def put(self, orderId, orderStatus):
        order = Order.get_by_id(orderId)
        order.status_order_id = orderStatus
        order.save()

        # change the hardcoded client_id
        # results = Order.query.filter_by(client_id=1).all()
        # orders = objetIntoJson(results)
        # socketio.emit("get-customer-orders",
        #               {"orders": orders}, namespace="/customer-orders")

        get_custormer_orders()

        return jsonify(message="Order updated!", status_code=200)


api.add_resource(KitchenOrdersUpdateOrderResource,
                 "/kitchen/orders/update-status/<int:orderId>/<int:orderStatus>", endpoint="orders_update-order-status")

# func


def objetIntoJson(dataObject):
    # Convierte los resultados en un formato JSON
    orders = []
    order_headers = []
    for result in dataObject:
        order = {
            "id": result.id,
            # "date": result.date,
            "total": result.total,
            "status_order_id": result.status_order_id,
            "client_id": result.client_id
        }
        order_body = []
        for itemmenu in result.order_menu:
            menu = {
                "id": itemmenu.id,
                "quantity": itemmenu.quantity,
                "subtotal": itemmenu.subtotal,
                "image": itemmenu.menu.image,
                "description": itemmenu.menu.description,
                "price": itemmenu.menu.price,
                "menu_name": itemmenu.menu.name
            }
            order_body.append(menu)
        order["body"] = order_body
        orders.append(order)
    return orders


clientId = 1
# socket


@socketio.on('message', namespace="/customer-orders")
def get_custormer_orders():
    # clientId should be in a session to get it anywhere
    results = Order.query.filter_by(client_id=clientId).all()
    orders = objetIntoJson(results)

    emit("get-customer-orders", {"orders": orders},
         namespace="/customer-orders", broadcast=True)
