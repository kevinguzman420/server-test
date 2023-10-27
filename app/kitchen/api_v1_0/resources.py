from app.db import db
from app.kitchen.api_v1_0.schemas import MenuSchema, ExtrasCategorySchema, ExtrasSchema, OrderByCustomerSchema
from app.users.models import Users
from app.kitchen.models import Order, OrderMenu, Menu, ExtrasCategory, Extras, OrderMenuExtras, StatusOrder
from . import kitchen_bp
from flask import request, jsonify, current_app
from flask_restful import Api, Resource
from datetime import date
import logging

from sqlalchemy import text

# blueprints

# models

# schemas

# misc

logger = logging.getLogger(__name__)
api = Api(kitchen_bp)

# status order | postman


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
    def get(self):
        menus = Menu.get_all()
        menus = MenuSchema(many=True).dump(menus)
        return jsonify(menus=menus, status_code=200)

    def post(self):
        menu = Menu(**request.json)
        menu.save()
        return jsonify(message="Menu created successfully", status_code=201)


api.add_resource(KitchenMenuResource, "/kitchen/menu", endpoint="kitchen_menu")

# orders


class KitchenOrdersResource(Resource):
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


class KitchenOrdersByCustomerResource(Resource):
    def get(self):
        # with current_app.app_context():
        #     sql_query = text('SELECT * FROM order;')
        #     res = db.session.execute(sql_query)
        #     print(res)

        return jsonify(message="It Works!", status_code=200)

        # results = Order.query.filter_by(client_id=1).join(OrderMenu).filter(
        #     OrderMenu.order_id == Order.id).all().to_json()

        # result_json = []

        # print(results)

        # for order, order_menu, menu in results:
        #     order_dict = {
        #         'order_id': order.id,
        #         'client_id': order.client_id,
        #         'status_order_id': order.status_order_id,
        #         'menu_id': menu.id,
        #         'menu_name': menu.name,
        #         'quantity': order_menu.quantity
        #     }
        #     result_json.append(order_dict)

        # return jsonify(result_json)


api.add_resource(KitchenOrdersByCustomerResource,
                 "/kitchen/orders-by-customer", endpoint="orders_by_customer")
