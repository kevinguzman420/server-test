from . import BaseTestClass

from app.kitchen.models import ExtrasCategory
from app.rol.models import Rol
from app.users.models import Users


class KitchenTestCase(BaseTestClass):

    # menu
    def test_kitchen_menu(self):
        res = self.client.post("/api/v1.0/kitchen/menu", json={
                               "name": "Chapina Chorizo", "description": "Doble Torta de carne Premium Blend, Queso Americano, Chorizo asado, Salsa Chicharronera, Tomate, Cebolla y Fresca Lechuga. Incluye Curly Fries y Frezka Natural.", "price": "64.00"})
        self.assertEqual(201, res.json["status_code"])
        self.assertEqual("Menu created successfully", res.json["message"])

    def test_kitchen_menu_get_all(self):
        # create one
        res = self.client.post("/api/v1.0/kitchen/menu", json={
                               "name": "Chapina Chorizo", "description": "Doble Torta de carne Premium Blend, Queso Americano, Chorizo asado, Salsa Chicharronera, Tomate, Cebolla y Fresca Lechuga. Incluye Curly Fries y Frezka Natural.", "price": "64.00"})
        self.assertEqual(201, res.json["status_code"])
        self.assertEqual("Menu created successfully", res.json["message"])

        # get all
        res = self.client.get("/api/v1.0/kitchen/menu")
        self.assertEqual(200, res.status_code)
        self.assertEqual(1, len(res.json["menus"]))

    # extra category
    def test_kitchen_extra_category_create(self):
        res = self.client.post(
            "/api/v1.0/kitchen/extras-category", json={"name": "Bebidas"})
        self.assertEqual("Extra category created successfully",
                         res.json["message"])
        self.assertEqual(201, res.json["status_code"])

    def test_kitchen_extras_category_get_all(self):
        res = self.client.get("/api/v1.0/kitchen/extras-category")
        self.assertEqual(200, res.status_code)
        self.assertIn("extras_category", res.json)

    # extras
    def test_kitchen_extra_create(self):
        # create extra category
        with self.app.app_context():
            ec = ExtrasCategory(name="Bebidas")
            ec.save()

            res = self.client.post("/api/v1.0/kitchen/extras", json={
                                   "name": "Bebidas de naranja", "price": 12.5, "extras_category_id": ec.id})
            self.assertEqual(201, res.json["status_code"])

    def test_kitchen_extra_get_all(self):
        res = self.client.get("/api/v1.0/kitchen/extras")
        self.assertEqual(200, res.status_code)
        self.assertIn("extras", res.json)

    # order
    def test_kitchen_order_create(self):
        pass
