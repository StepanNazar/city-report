import unittest

from config import TestConfig
from werkzeug.test import TestResponse

from api import create_app, db
from api.blueprints.auth.models import User


class TestAuth(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def register(
        self,
        firstname: str = "test",
        lastname: str = "test",
        email: str = "test@gmail.com",
        password: str = "Pas$word123",  # noqa: S107
    ) -> TestResponse:
        return self.client.post(
            "/register",
            json={
                "name": firstname,
                "lastName": lastname,
                "email": email,
                "password": password,
            },
        )

    def login(
        self,
        email: str = "test@gmail.com",
        password: str = "Pas$word123",  # noqa: S107
    ) -> TestResponse:
        return self.client.post("/login", json={"email": email, "password": password})

    def check_refresh_cookie(self, response: TestResponse):
        cookie = response.headers["Set-Cookie"]
        path = next(filter(lambda x: x.strip().startswith("Path"), cookie.split(";")))
        self.assertEqual("/refresh", path.split("=")[1])

    def test_register(self):
        response = self.register()
        self.assertEqual(201, response.status_code)
        json = response.get_json()
        self.assertIn("access_token", json)
        self.check_refresh_cookie(response)
        # test for email already used
        response = self.register()
        self.assertEqual(409, response.status_code)
        # test for invalid email
        response = self.register(email="test")
        self.assertEqual(422, response.status_code)

    def test_login_and_refresh(self):
        self.register()
        response = self.login()
        self.assertEqual(200, response.status_code)
        json = response.get_json()
        self.assertIn("access_token", json)
        self.check_refresh_cookie(response)
        response = self.client.get("/refresh")
        self.assertEqual(200, response.status_code)
        json = response.get_json()
        self.assertIn("access_token", json)
        response = self.login(email="test")
        self.assertEqual(422, response.status_code)
        response = self.login(email="test@x.com")
        self.assertEqual(401, response.status_code)

    def test_logout_with_access_token(self):
        response = self.register()
        access_token = response.get_json()["access_token"]
        response = self.client.post(
            "/logout", headers={"Authorization": f"Bearer {access_token}"}
        )
        self.assertEqual(200, response.status_code)
        response = self.client.get("/refresh")
        self.assertEqual(401, response.status_code)

    def test_logout_with_refresh_token(self):
        self.register()
        response = self.client.post("/logout")
        self.assertEqual(200, response.status_code)
        response = self.client.get("/refresh")
        self.assertEqual(401, response.status_code)

    def test_whoami(self):
        response = self.register()
        access_token = response.get_json()["access_token"]
        response = self.client.get(
            "/whoami", headers={"Authorization": f"Bearer {access_token}"}
        )
        self.assertEqual(200, response.status_code)
        json = response.get_json()
        for field in ["name", "email", "id", "lastName", "isActivated"]:
            self.assertIn(field, json)
        response = self.client.get("/whoami")  # no credentials
        self.assertEqual(401, response.status_code)

    def test_activate(self):
        with self.app.app_context():
            self.register()
            user: User | None = (
                db.session.query(User).filter_by(email="test@gmail.com").first()
            )
            if user is None:
                self.fail("User not found in the database")
            self.assertFalse(user.is_activated)
            response = self.client.get(f"/activate/{user.activation_code}")
            self.assertEqual(200, response.status_code)
            # update user from db
            db.session.refresh(user)
            self.assertTrue(user.is_activated)
            # test for already activated
            response = self.client.get(f"/activate/{user.activation_code}")
            self.assertEqual(404, response.status_code)
            # test for invalid code
            response = self.client.get("/activate/123")
            self.assertEqual(404, response.status_code)

    def test_send_activation_link(self):
        with self.app.app_context():
            response = self.register()
            access_token = response.get_json()["access_token"]
            response = self.client.post(
                "/send-activation-link",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            self.assertEqual(202, response.status_code)
            # test refusing to send link to already activated user
            user: User | None = (
                db.session.query(User).filter_by(email="test@gmail.com").first()
            )
            if user is None:
                self.fail("User not found in the database")
            self.client.get(f"/activate/{user.activation_code}")
            response = self.client.post(
                "/send-activation-link",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            self.assertEqual(409, response.status_code)
            response = self.client.post("/send-activation-link")  # no credentials
            self.assertEqual(401, response.status_code)

    def test_get_all_devices(self):
        # login 3 devices
        self.register()
        self.login()
        response = self.login()
        access_token = response.get_json()["access_token"]
        response = self.client.get(
            "/devices", headers={"Authorization": f"Bearer {access_token}"}
        )
        self.assertEqual(200, response.status_code)
        json = response.get_json()
        self.assertEqual(3, len(json))
        device = json[0]
        for fields in ["id", "ip", "device", "os", "browser", "loginTime"]:
            self.assertIn(fields, device)
        response = self.client.get("/devices")  # no credentials
        self.assertEqual(401, response.status_code)

    def test_logout_all_devices(self):
        # login 3 devices
        self.register()
        self.login()
        response = self.login()
        access_token = response.get_json()["access_token"]
        response = self.client.delete(
            "/devices", headers={"Authorization": f"Bearer {access_token}"}
        )
        self.assertEqual(200, response.status_code)
        # check if this device is logged out
        response = self.client.get("/refresh")
        self.assertEqual(401, response.status_code)
        # check if other devices were logged out
        response = self.login()
        access_token = response.get_json()["access_token"]
        response = self.client.get(
            "/devices", headers={"Authorization": f"Bearer {access_token}"}
        )
        json = response.get_json()
        self.assertEqual(1, len(json))  # only new device is logged in
        response = self.client.delete("/devices")  # no credentials
        self.assertEqual(401, response.status_code)

    def test_logout_device(self):
        response = self.register()
        # get access and refresh tokens of 1st device
        access_token = response.get_json()["access_token"]
        refresh_token = response.headers["Set-Cookie"].split("=")[1].split(";")[0]
        # login 2nd device and logout 1st device
        response = self.login()
        access_token2 = response.get_json()["access_token"]
        response = self.client.delete(
            "/devices/1",
            headers={"Authorization": f"Bearer {access_token2}"},
            json={"password": "Pas$word123"},
        )
        self.assertEqual(204, response.status_code)
        # check if 1st device is logged out
        response = self.client.get(
            "/refresh", headers={"Cookie": f"refresh_token={refresh_token}"}
        )
        self.assertEqual(401, response.status_code)
        response = self.client.get(
            "/whoami", headers={"Authorization": f"Bearer {access_token}"}
        )
        self.assertEqual(401, response.status_code)
        # check if 2nd device is still logged in
        response = self.client.get(
            "/whoami", headers={"Authorization": f"Bearer {access_token2}"}
        )
        self.assertEqual(200, response.status_code)
        response = self.client.delete(
            "/devices/1", json={"password": "Pas$word123"}
        )  # no credentials
        self.assertEqual(401, response.status_code)

    def test_reset_password(self):
        pass

    def test_send_reset_password_link(self):
        pass

    def test_change_password(self):
        pass


if __name__ == "__main__":
    unittest.main()
