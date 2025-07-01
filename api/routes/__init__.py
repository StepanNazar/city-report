from flask_jwt_extended.exceptions import JWTExtendedException
from jwt import PyJWTError

from .admin import admin
from .ai_comments import ai_comments
from .auth import auth
from .comments import comments
from .locations import locations
from .posts import posts
from .solutions import solutions
from .uploads import uploads
from .users import users

authorizations = {
    "jwt_access_token": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"},
    "jwt_refresh_token": {
        "type": "apiKey",
        "in": "cookie",
        "name": "refresh_token_cookie",
    },
    "csrf_refresh_token": {
        "type": "apiKey",
        "in": "header",
        "name": "X-CSRF-TOKEN",
    },
}


def register_routes(app):
    """Register all routes for the API."""
    app.security_schemes = authorizations
    app.register_blueprint(admin)
    app.register_blueprint(ai_comments)
    app.register_blueprint(auth)
    app.register_blueprint(comments)
    app.register_blueprint(locations)
    app.register_blueprint(posts)
    app.register_blueprint(solutions)
    app.register_blueprint(uploads)
    app.register_blueprint(users)

    @app.errorhandler(PyJWTError)
    @app.errorhandler(JWTExtendedException)
    def handle_jwt_errors(error):
        return {"message": str(error)}, 401
