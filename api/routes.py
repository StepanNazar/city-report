import datetime
from uuid import uuid4

import requests
from flask import request, jsonify, Response
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    set_refresh_cookies,
    unset_jwt_cookies,
    get_current_user, get_jwt, get_jti, get_jwt_identity
)
from flask_restx import Resource

from main import api, jwt, app, db
from models import User, ActiveDevice
from services import EmailService


@jwt.user_identity_loader
def user_identity_lookup(user: User) -> str:
    return str(user.id)


@jwt.user_lookup_loader
def user_lookup_callback(jwt_header, jwt_data: dict) -> User:
    identity = jwt_data["sub"]
    return User.query.filter_by(id=int(identity)).one_or_none()


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
        access_jti=get_jti(access_token),
        expires_at=datetime.datetime.now(datetime.UTC) + app.config['JWT_REFRESH_TOKEN_EXPIRES']
    )
    db.session.add(active_device)
    db.session.commit()
    response = jsonify({'access_token': access_token})
    set_refresh_cookies(response, refresh_token)
    return response


@api.route('/register')
class Register(Resource):
    def post(self):
        data = request.get_json()
        current_user = User.query.filter_by(email=data.get('email')).first()
        if current_user:
            return {'error': 'Email already used'}, 409

        new_user = User(firstname=data.get('name'),
                        lastname=data.get('lastName'),
                        email=data.get('email'),
                        activation_code=str(uuid4()))
        new_user.set_password(data.get('password'))
        db.session.add(new_user)
        db.session.commit()

        # what if exceptions happens below and user is saved to db, but no link and token sent?
        response = generate_jwt_tokens(new_user)
        response.status_code = 201
        EmailService().send_activation_link(new_user)
        return response


@api.route("/login")
class Login(Resource):
    def post(self):
        data = request.get_json()
        db_user = User.query.filter_by(email=data.get('email')).first()
        if db_user and db_user.check_password(data.get('password')):
            return generate_jwt_tokens(db_user)
        return {"message": "Invalid username or password"}, 401


@api.route('/refresh')
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


@api.route('/logout')
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


@api.route('/activate/<string:activation_code>')
class Activate(Resource):
    def get(self, activation_code):
        user = User.query.filter_by(activation_code=activation_code).first()
        if user:
            user.is_activated = True
            db.session.commit()
            return {'message': 'User activated'}, 200
        return {'error': 'User not found'}, 404


@api.route('/send-activation-link')
class SendActivationLink(Resource):
    @jwt_required()
    def post(self):
        current_user = get_current_user()
        if current_user.is_activated:
            return {'error': 'User already activated'}, 409
        EmailService().send_activation_link(current_user)
        return {}, 202


@api.route('/whoami')
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


@api.route('/devices')  # to do make consistent case(camelCase or snake_case) in api
class Devices(Resource):
    @jwt_required()
    def get(self):
        current_user = get_current_user()
        return jsonify([{"id": device.id, "ip": device.ip_address, "device": device.device,
                         "os": device.os, "browser": device.browser,
                         "loginTime": device.login_time}
                        for device in current_user.active_devices])


@api.route('/devices/<int:device_id>')
class Device(Resource):
    @jwt_required()
    def delete(self, device_id):
        current_user = get_current_user()
        device = ActiveDevice.query.filter_by(id=device_id, user_id=current_user.id).first()
        if device:
            db.session.delete(device)
            db.session.commit()
            return {}, 204
        return {'error': 'Device not found'}, 404


@api.route('/posts')
class Posts(Resource):
    def get(self):
        return [
            {
                "id": 1,
                "authorID": 8,
                "authorName": "John",
                "creationTime": "2025-01-22 22:17",
                "latitude": 45.8548,
                "longitude": 89.6545,
                "title": "Lorem",
            }
        ]

    def post(self):
        return {}, 201


@api.route('/posts/<int:post_id>')
class Post(Resource):
    def get(self, post_id):
        return {
            "id": 1,
            "authorID": 8,
            "authorName": "John",
            "creationTime": "2025-01-22 22:17",
            "latitude": 45.8548,
            "longitude": 89.6545,
            "country": "ukraine",
            "state": "if oblast",
            "locality": "if",
            "title": "Lorem",
            "body": "lorem"
        }

    def patch(self, post_id):
        return {}, 204

    def delete(self, post_id):
        return {}, 204


# com struct {
# comId
# postID
# who create
# body
# countof likes dislikes
# }
@api.route('/comentsForId')
class ComentsForId(Resource):
    def get(self):
        com_id = request.args.get('id', type=int, default=0)  # Отримуємо параметр id
        if com_id <= 0:
            return jsonify({"error": "Invalid ID"}), 400  # Перевірка на валідність id

        # Формуємо URL для отримання коментарів
        url = f"https://jsonplaceholder.typicode.com/posts/{com_id}/comments"

        try:
            # Виконуємо GET-запит до JSONPlaceholder
            response = requests.get(url)
            response.raise_for_status()  # Перевіряємо статус відповіді (404, 500 тощо)

            # Повертаємо отримані дані у вигляді JSON
            return jsonify(response.json())
        except:
            return jsonify({"error": "Failed to fetch comments"}), 500


@api.route('/password')
class ChangePassword(Resource):
    @jwt_required()
    def patch(self):
        return {}, 204


@api.route('/password/reset-request')
class ResetPasswordRequest(Resource):
    @jwt_required()
    def post(self):
        return {}, 202


@api.route('/password/reset')
class ResetPassword(Resource):
    @jwt_required()
    def post(self):
        return {}, 204
