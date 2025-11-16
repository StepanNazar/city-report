from apiflask import abort
from apiflask.views import MethodView
from email_validator import EmailNotValidError
from flask import Response, jsonify, make_response, request, url_for
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

from api import db, jwt
from api.blueprints.auth import auth
from api.blueprints.auth.models import ActiveDevice, User
from api.blueprints.auth.schemas import (
    AccessTokenSchema,
    DeviceSchema,
    LoginSchema,
    PasswordSchema,
    RegisterSchema,
    WhoAmISchema,
)
from api.blueprints.locations.routes import get_or_create_locality
from api.services import EmailService


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


class Register(MethodView):
    @auth.input(RegisterSchema)
    @auth.output(AccessTokenSchema, status_code=201)
    @auth.doc(
        responses={
            400: "Invalid email or locality_id",
            409: "Email already used",
            201: "User registered",
        },
    )
    def post(self, json_data):
        """Register a new user. Set refresh token cookie. Send the activation link."""
        email = json_data.get("email")
        try:
            current_user = User.find_by_email(email)
            if current_user:
                abort(409, message="Email already used")
        except EmailNotValidError as e:
            abort(400, message=f"Invalid email address: {e}")

        locality_id = json_data.get("locality_id")
        locality_provider = json_data.get("locality_provider")
        inner_locality_id = None
        if locality_id and locality_provider:
            locality = get_or_create_locality(locality_id, locality_provider)
            inner_locality_id = locality.id

        new_user = User(
            firstname=json_data.get("first_name"),
            lastname=json_data.get("last_name"),
            email=email,
            password=json_data.get("password"),
            locality_id=inner_locality_id,
        )
        db.session.add(new_user)
        db.session.commit()

        # what if exceptions happens below and user is saved to db, but no link and token sent?
        response = generate_jwt_tokens(new_user)
        response.status_code = 201
        response.headers["Location"] = url_for("users.user", user_id=new_user.id)
        # EmailService().send_activation_link(new_user)
        return response


class Login(MethodView):
    @auth.input(LoginSchema)
    @auth.output(AccessTokenSchema)
    @auth.doc(
        responses={401: "Invalid email or password", 200: "User logged in"},
    )
    def post(self, json_data):
        """Login user. Set refresh token cookie."""
        json_data = request.get_json()
        try:
            db_user = User.find_by_email(json_data.get("email"))
        except EmailNotValidError:
            abort(401, message="Invalid username or password")
        if db_user and db_user.check_password(json_data.get("password")):
            return generate_jwt_tokens(db_user)
        abort(401, message="Invalid username or password")


class Refresh(MethodView):
    @jwt_required(refresh=True)
    @auth.output(AccessTokenSchema)
    @auth.doc(
        security=["jwt_refresh_token", "csrf_refresh_token"],
        responses={200: "Access token refreshed"},
    )
    def post(self):
        """Refresh access token"""
        identity = get_jwt_identity()
        token = get_jwt()
        access_token = create_access_token(identity=identity)
        ActiveDevice.query.filter_by(refresh_jti=token["jti"]).update(
            {"access_jti": get_jti(access_token)}
        )
        db.session.commit()
        return jsonify({"access_token": access_token})


class Logout(MethodView):
    @jwt_required()
    @auth.doc(security=["jwt_access_token"])
    def post(self):
        """Log out from the current device. Unset refresh token cookie."""
        token = get_jwt()
        if token["type"] == "access":
            ActiveDevice.query.filter_by(access_jti=token["jti"]).delete()
        else:
            ActiveDevice.query.filter_by(refresh_jti=token["jti"]).delete()
        db.session.commit()
        response = jsonify({"message": "Logged out"})
        unset_jwt_cookies(response)
        return response


class Activate(MethodView):
    @auth.doc(
        security=[], responses={400: "Invalid activation code", 200: "User activated"}
    )
    def post(self, activation_code):
        """Activate the user's account"""
        user = User.query.filter_by(activation_code=activation_code).first()
        if user and not user.is_activated:
            user.is_activated = True
            db.session.commit()
            return {"message": "User activated"}
        abort(400, message="Invalid activation code")


class SendActivationLink(MethodView):
    @jwt_required()
    @auth.doc(
        responses={409: "User already activated", 202: "Activation link sent"},
        security=["jwt_access_token"],
    )
    def post(self):
        """Request activation link"""
        current_user = get_current_user()
        if current_user.is_activated:
            abort(409, message="User already activated")
        EmailService().send_activation_link(current_user)
        return {}, 202


class WhoAmI(MethodView):
    @jwt_required()
    @auth.output(WhoAmISchema)
    @auth.doc(security="jwt_access_token")
    def get(self):
        """Get current user info"""
        return get_current_user()


class Devices(MethodView):
    @jwt_required()
    @auth.output(DeviceSchema(many=True))
    @auth.doc(security="jwt_access_token")
    def get(self):
        """Get all active devices"""
        return get_current_user().active_devices

    @jwt_required()
    @auth.doc(
        security="jwt_access_token", responses={204: "Logged out from all devices"}
    )
    def delete(self):
        """Log out from all devices"""
        identity = get_jwt_identity()
        ActiveDevice.query.filter_by(user_id=int(identity)).delete()
        db.session.commit()
        response = make_response("", 204)
        unset_jwt_cookies(response)
        return response


class Device(MethodView):
    @jwt_required()
    @auth.input(PasswordSchema)
    @auth.doc(
        responses={
            401: "Invalid password",
            404: "Device not found",
            204: "Device logged out",
        },
        security=["jwt_access_token"],
    )
    def delete(self, device_id, json_data):
        """Log out from the device"""
        current_user = get_current_user()
        password = json_data.get("password")
        if not current_user.check_password(password):
            abort(401, message="Invalid password")
        device = ActiveDevice.query.filter_by(
            id=device_id, user_id=current_user.id
        ).first()
        if device:
            db.session.delete(device)
            db.session.commit()
            return {}, 204
        abort(404, message="Device not found")


class ChangePassword(MethodView):
    @jwt_required()
    @auth.doc(
        security="jwt_access_token",
        responses={204: "Password changed", 400: "Invalid old or new password"},
    )
    def put(self):
        """Change password"""
        return {}, 501


class ResetPasswordRequest(MethodView):
    @auth.doc(responses={202: "Password reset link sent"})
    def post(self):
        """Request email with a secret code for password reset"""
        return {}, 501


class ResetPassword(MethodView):
    @auth.doc(
        responses={204: "Password changed", 400: "Invalid secret code or new password"}
    )
    def post(self):
        """Reset password using a secret code from email and pass a new password"""
        return {}, 501


auth.add_url_rule("/register", view_func=Register.as_view("register"))
auth.add_url_rule("/login", view_func=Login.as_view("login"))
auth.add_url_rule("/refresh", view_func=Refresh.as_view("refresh"))
auth.add_url_rule("/logout", view_func=Logout.as_view("logout"))
auth.add_url_rule(
    "/activate/<uuid:activation_code>", view_func=Activate.as_view("activate")
)
auth.add_url_rule(
    "/activation-link-email",
    view_func=SendActivationLink.as_view("send_activation_link"),
)
auth.add_url_rule("/whoami", view_func=WhoAmI.as_view("whoami"))
auth.add_url_rule("/devices", view_func=Devices.as_view("all_devices"))
auth.add_url_rule("/devices/<int:device_id>", view_func=Device.as_view("device"))
auth.add_url_rule("/password", view_func=ChangePassword.as_view("change_password"))
auth.add_url_rule(
    "/password/reset-request",
    view_func=ResetPasswordRequest.as_view("reset_password_request"),
)
auth.add_url_rule("/password/reset", view_func=ResetPassword.as_view("reset_password"))
