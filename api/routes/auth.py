from email_validator import EmailNotValidError
from flask import request, jsonify, Response
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    set_refresh_cookies,
    unset_jwt_cookies,
    get_current_user, get_jwt, get_jti
)
from flask_restx import Resource, Namespace

from api import jwt, db
from api.models import User, ActiveDevice
from api.services import EmailService

# later path can be changed to /auth, but kept as / for now to match the frontend
auth = Namespace('auth', description='Authentication operations', path='/')


@jwt.user_identity_loader
def user_identity_lookup(user: User) -> str:
    return str(user.id)


@jwt.user_lookup_loader
def user_lookup_callback(jwt_header, jwt_data: dict) -> User:
    identity = jwt_data["sub"]
    return User.query.get(int(identity))


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    if jwt_payload['type'] == 'refresh':
        token = ActiveDevice.query.filter_by(refresh_jti=jwt_payload['jti']).one_or_none()
    else:
        token = ActiveDevice.query.filter_by(access_jti=jwt_payload['jti']).one_or_none()
    return token is None


def generate_jwt_tokens(user: User) -> Response:
    refresh_token = create_refresh_token(identity=user)
    access_token = create_access_token(identity=user)
    active_device = ActiveDevice(
        user_agent=request.user_agent.string,
        ip_address=request.remote_addr,
        user_id=user.id,
        refresh_jti=get_jti(refresh_token),
        access_jti=get_jti(access_token)
    )
    db.session.add(active_device)
    db.session.commit()
    response = jsonify({'access_token': access_token})
    set_refresh_cookies(response, refresh_token)
    return response


@auth.route('/register')
class Register(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        try:
            current_user = User.find_by_email(email)
            if current_user:
                return {'error': 'Email already used'}, 409
            new_user = User(firstname=data.get('name'), lastname=data.get('lastName'),
                            email=email, password=data.get('password'))
        except EmailNotValidError as e:
            return {'error': f'Invalid email address: {e}'}, 400
        except AssertionError as e:
            return {'error': str(e)}, 400
        db.session.add(new_user)
        db.session.commit()

        # what if exceptions happens below and user is saved to db, but no link and token sent?
        response = generate_jwt_tokens(new_user)
        response.status_code = 201
        EmailService().send_activation_link(new_user)
        return response


@auth.route("/login")
class Login(Resource):
    def post(self):
        data = request.get_json()
        try:
            db_user = User.find_by_email(data.get('email'))
        except EmailNotValidError as e:
            return {"message": "Invalid username or password"}, 401
        if db_user and db_user.check_password(data.get('password')):
            return generate_jwt_tokens(db_user)
        return {"message": "Invalid username or password"}, 401


@auth.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def get(self):
        current_user = get_current_user()
        token = get_jwt()
        access_token = create_access_token(identity=current_user)
        ActiveDevice.query.filter_by(refresh_jti=token['jti']).update(
            {"access_jti": get_jti(access_token)}
        )
        db.session.commit()
        return jsonify({'access_token': access_token})


@auth.route('/logout')
class Logout(Resource):
    # verify_type=False should allow to logout from both access and refresh tokens
    # but it doesn't work as expected and returns 401 when there is only refresh token
    @jwt_required(verify_type=False)
    def post(self):
        token = get_jwt()
        if token['type'] == 'access':
            ActiveDevice.query.filter_by(access_jti=token['jti']).delete()
        else:
            ActiveDevice.query.filter_by(refresh_jti=token['jti']).delete()
        db.session.commit()
        response = jsonify({'message': 'Logged out'})
        unset_jwt_cookies(response)
        return response


@auth.route('/activate/<string:activation_code>')
class Activate(Resource):
    def get(self, activation_code):
        user = User.query.filter_by(activation_code=activation_code).first()
        if user and not user.is_activated:
            user.is_activated = True
            db.session.commit()
            return {'message': 'User activated'}, 200
        return {'error': 'User not found'}, 404


@auth.route('/send-activation-link')
class SendActivationLink(Resource):
    @jwt_required()
    def post(self):
        current_user = get_current_user()
        if current_user.is_activated:
            return {'error': 'User already activated'}, 409
        EmailService().send_activation_link(current_user)
        return {}, 202


@auth.route('/whoami')
class WhoAmI(Resource):
    @jwt_required()
    def get(self):
        current_user = get_current_user()
        return {
            "id": current_user.id,
            "name": current_user.firstname,
            "lastName": current_user.lastname,
            "email": current_user.email,
            "isActivated": current_user.is_activated
        }


@auth.route('/devices')  # to do make consistent case(camelCase or snake_case) in api
class Devices(Resource):
    @jwt_required()
    def get(self):
        current_user = get_current_user()
        return jsonify([{"id": device.id, "ip": device.ip_address, "device": device.device,
                         "os": device.os, "browser": device.browser,
                         "loginTime": device.login_time}
                        for device in current_user.active_devices])

    @jwt_required()
    def delete(self):
        """Logout from all devices"""
        current_user = get_current_user()
        ActiveDevice.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        response = jsonify({'message': 'Logged out from all devices'})
        unset_jwt_cookies(response)
        return response


@auth.route('/devices/<int:device_id>')
class Device(Resource):
    @jwt_required()
    def delete(self, device_id):
        current_user = get_current_user()
        password = request.get_json().get('password')
        if not current_user.check_password(password):
            return {'error': 'Invalid password'}, 401
        device = ActiveDevice.query.filter_by(id=device_id, user_id=current_user.id).first()
        if device:
            db.session.delete(device)
            db.session.commit()
            return {}, 204
        return {'error': 'Device not found'}, 404


@auth.route('/password')
class ChangePassword(Resource):
    @jwt_required()
    def patch(self):
        return {}, 204


@auth.route('/password/reset-request')
class ResetPasswordRequest(Resource):
    @jwt_required()
    def post(self):
        return {}, 202


@auth.route('/password/reset')
class ResetPassword(Resource):
    @jwt_required()
    def post(self):
        return {}, 204
