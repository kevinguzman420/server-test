import unittest
from app import create_app, db
from app.rol.models import Rol
from app.users.models import Users


class BaseTestClass(unittest.TestCase):
    def setUp(self):
        self.app = create_app(settings_module='config.testing')
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            # create an admin user
            rol = BaseTestClass.create_rol("default-rol")
            BaseTestClass.create_user(
                "KevinG", "kevin@gmail.com", "test", rol.id)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    @staticmethod
    def create_rol(name):
        rol = Rol(name=name)
        rol.save()
        return rol

    @staticmethod
    def create_user(username, email, password, rol_id):
        user = Users(username=username, email=email, rol_id=rol_id)
        user.generate_password(password)
        user.save()
        return user
