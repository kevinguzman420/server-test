from . import BaseTestClass


class RolTestCase(BaseTestClass):

    def test_rol_create(self):
        res = self.client.post("/api/v1.0/rol", json={"name": "user"})
        self.assertEqual(201, res.json["status_code"])
        self.assertEqual("Rol created successfully", res.json["message"])

    def test_rol_get_all(self):
        res = self.client.get("/api/v1.0/rol")
        self.assertEqual(200, res.status_code)

    def test_rol_get_one(self):
        res = self.client.post("/api/v1.0/rol", json={"name": "user2"})
        self.assertEqual(201, res.json["status_code"])

        res = self.client.get("/api/v1.0/rol/1")
        self.assertEqual(200, res.status_code)

    def test_rol_delete_one(self):
        res = self.client.post("/api/v1.0/rol", json={"name": "user3"})
        self.assertEqual(201, res.json["status_code"])

        # 2: is the rol created above
        res = self.client.delete("/api/v1.0/rol/2")
        self.assertEqual(200, res.status_code)
