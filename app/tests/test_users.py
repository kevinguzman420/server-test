from . import BaseTestClass
from app.users.models import Users
from app.rol.models import Rol

class UsersTestCase(BaseTestClass):

    def test_users_create_one(self):
        # rol
        with self.app.app_context():
            rol = Rol.get_by_id(1)
            # user
            user_data = {"username": "username", "email": "email@example.com", "rol_id": 1}
            user = Users(**user_data)
            user.generate_password("test")
            user.save()
            self.assertEqual("username", user.username)
            self.assertEqual(1, user.rol_id)
    
    def test_users_change_rol(self):
        # rol
        with self.app.app_context():
            # change rol
            rol = Rol(name="user_user")
            rol.save()
            self.assertEqual(2, rol.id)

            user_data = {"username": "username1", "email": "email2@example.com", "rol_id": 1}
            user = Users(**user_data)
            user.generate_password("test")
            user.save()
            self.assertEqual("username1", user.username)
            self.assertEqual(1, user.rol_id)

            user = Users.get_by_id(1)
            user.rol_id = rol.id
            user.save()
            self.assertEqual(2, user.rol_id)


    def test_users_get_all(self):
        res = self.client.get('/api/v1.0/users')
        self.assertEqual(200, res.status_code)