from email_validator import EmailNotValidError
from flask import Response, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    get_jti,
    get_jwt,
    get_jwt_identity,
    jwt_required,
    set_refresh_cookies,
    unset_jwt_cookies,
)
from flask_restx import Namespace, Resource, fields

from api import db, jwt, models
from api.models import ActiveDevice, User
from api.services import EmailService

# later path can be changed to /auth, but kept as / for now to match the frontend
auth = Namespace("auth", description="Authentication operations", path="/")

access_token_model = auth.model(
    "AccessToken", {"access_token": fields.String(required=True)}
)
password_model = auth.model(
    "Password",
    {
        "password": fields.String(
            required=True,
            min_length=8,
            max_length=models.PASSWORD_MAX_LENGTH,
            # pattern="^regex$", validate in both api and database?
            example="Pas$word123",
        )
    },
)
login_model = auth.inherit(
    "Login",
    password_model,
    {
        "email": fields.String(required=True, example="dsx@gmail.com"),
    },
)
register_model = auth.inherit(
    "Register",
    login_model,
    {
        "name": fields.String(required=True, description="first name", example="John"),
        "lastName": fields.String(
            required=True, description="last name", example="Doe"
        ),
    },
)
user_model = auth.model(
    "User",
    {
        "id": fields.Integer(),
        "name": fields.String(attribute="firstname"),
        "lastName": fields.String(attribute="lastname"),
        "email": fields.String(),
        "isActivated": fields.Boolean(attribute="is_activated"),
    },
)
device_model = auth.model(
    "Device",
    {
        "id": fields.Integer(),
        "ip": fields.String(attribute="ip_address"),
        "device": fields.String(),
        "os": fields.String(),
        "browser": fields.String(),
        "loginTime": fields.DateTime(attribute="login_time"),
    },
)


@jwt.user_lookup_loader
def user_lookup_callback(jwt_header, jwt_data: dict) -> User | None:
    identity = jwt_data["sub"]
    return User.query.get(int(identity))  # legacy method query.get


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    if jwt_payload["type"] == "refresh":
        # additional checks can be added like user_agent?
        token = ActiveDevice.query.filter_by(
            refresh_jti=jwt_payload["jti"]
        ).one_or_none()
    else:
        token = ActiveDevice.query.filter_by(
            access_jti=jwt_payload["jti"]
        ).one_or_none()
    return token is None


def generate_jwt_tokens(user: User) -> Response:
    refresh_token = create_refresh_token(identity=str(user.id))
    access_token = create_access_token(identity=str(user.id))
    active_device = ActiveDevice(
        user_agent=request.user_agent.string,
        ip_address=request.remote_addr,
        user_id=user.id,
        refresh_jti=get_jti(refresh_token),
        access_jti=get_jti(access_token),
    )
    db.session.add(active_device)
    db.session.commit()
    response = jsonify({"access_token": access_token})
    set_refresh_cookies(response, refresh_token)
    return response


@auth.route("/register")
class Register(Resource):
    @auth.expect(register_model)
    @auth.doc(
        responses={400: "Invalid email or password", 409: "Email already used"},
        security=[],
    )
    @auth.response(201, "User registered", access_token_model)
    def post(self):
        """Register a new user. Sets refresh token cookie. Sends activation link."""
        data = request.get_json()
        email = data.get("email")
        try:
            current_user = User.find_by_email(email)
            if current_user:
                return {"message": "Email already used"}, 409
            new_user = User(
                firstname=data.get("name"),
                lastname=data.get("lastName"),
                email=email,
                password=data.get("password"),
            )
        except EmailNotValidError as e:
            return {"message": f"Invalid email address: {e}"}, 400
        except AssertionError as e:
            return {"message": str(e)}, 400
        db.session.add(new_user)
        db.session.commit()

        # what if exceptions happens below and user is saved to db, but no link and token sent?
        response = generate_jwt_tokens(new_user)
        response.status_code = 201
        EmailService().send_activation_link(new_user)
        return response


@auth.route("/login")
class Login(Resource):
    @auth.expect(login_model)
    @auth.doc(responses={401: "Invalid email or password"}, security=[])
    @auth.response(200, "User logged in", access_token_model)
    def post(self):
        """Login user. Sets refresh token cookie."""
        data = request.get_json()
        try:
            db_user = User.find_by_email(data.get("email"))
        except EmailNotValidError:
            return {"message": "Invalid username or password"}, 401
        if db_user and db_user.check_password(data.get("password")):
            return generate_jwt_tokens(db_user)
        return {"message": "Invalid username or password"}, 401


@auth.route("/refresh")
class Refresh(Resource):
    @jwt_required(refresh=True)
    @auth.doc(security="jwt_refresh_token")
    @auth.response(200, "Access token refreshed", access_token_model)
    def get(self):
        """Refresh access token"""
        identity = get_jwt_identity()
        token = get_jwt()
        access_token = create_access_token(identity=identity)
        ActiveDevice.query.filter_by(refresh_jti=token["jti"]).update(
            {"access_jti": get_jti(access_token)}
        )
        db.session.commit()
        return jsonify({"access_token": access_token})


@auth.route("/logout")
class Logout(Resource):
    # verify_type=False should allow to log out with both access and refresh tokens,
    # but it doesn't work as expected and returns 401 when there is only refresh token
    @jwt_required(verify_type=False)
    @auth.doc(security=["jwt_access_token", "jwt_refresh_token"])
    def post(self):
        """Log out from current device. Unsets refresh token cookie."""
        token = get_jwt()
        if token["type"] == "access":
            ActiveDevice.query.filter_by(access_jti=token["jti"]).delete()
        else:
            ActiveDevice.query.filter_by(refresh_jti=token["jti"]).delete()
        db.session.commit()
        response = jsonify({"message": "Logged out"})
        unset_jwt_cookies(response)
        return response


@auth.route("/activate/<string:activation_code>")
class Activate(Resource):
    @auth.doc(security=[], responses={404: "User not found", 200: "User activated"})
    def get(self, activation_code):
        """Activate user account"""
        user = User.query.filter_by(activation_code=activation_code).first()
        if user and not user.is_activated:
            user.is_activated = True
            db.session.commit()
            return {"message": "User activated"}
        return {"message": "User not found"}, 404


@auth.route("/send-activation-link")
class SendActivationLink(Resource):
    @jwt_required()
    @auth.doc(responses={409: "User already activated", 202: "Activation link sent"})
    def post(self):
        """Request activation link"""
        current_user = get_current_user()
        if current_user.is_activated:
            return {"message": "User already activated"}, 409
        EmailService().send_activation_link(current_user)
        return {}, 202


@auth.route("/whoami")
class WhoAmI(Resource):
    @jwt_required()
    @auth.marshal_with(user_model)
    def get(self):
        """Get current user info"""
        return get_current_user()


@auth.route("/devices")  # to do make consistent case(camelCase or snake_case) in api
class Devices(Resource):
    @jwt_required()
    @auth.marshal_list_with(device_model)
    def get(self):
        """Get all active devices"""
        return get_current_user().active_devices

    @jwt_required()
    def delete(self):
        """Log out from all devices"""
        identity = get_jwt_identity()
        ActiveDevice.query.filter_by(user_id=int(identity)).delete()
        db.session.commit()
        response = jsonify({"message": "Logged out from all devices"})
        unset_jwt_cookies(response)
        return response


@auth.route("/devices/<int:device_id>")
class Device(Resource):
    @jwt_required()
    @auth.expect(password_model)
    @auth.doc(
        responses={
            401: "Invalid password",
            404: "Device not found",
            204: "Device logged out",
        }
    )
    def delete(self, device_id):
        """Log out from device"""
        current_user = get_current_user()
        password = request.get_json().get("password")
        if not current_user.check_password(password):
            return {"message": "Invalid password"}, 401
        device = ActiveDevice.query.filter_by(
            id=device_id, user_id=current_user.id
        ).first()
        if device:
            db.session.delete(device)
            db.session.commit()
            return {}, 204
        return {"message": "Device not found"}, 404


@auth.route("/password")
class ChangePassword(Resource):
    @jwt_required()
    def patch(self):
        """Change password"""
        return {}, 501


@auth.route("/password/reset-request")
class ResetPasswordRequest(Resource):
    @jwt_required()
    def post(self):
        """Request password reset"""
        return {}, 501


@auth.route("/password/reset")
class ResetPassword(Resource):
    @jwt_required()
    def post(self):
        """Reset password"""
        return {}, 501
