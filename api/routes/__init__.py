from flask_jwt_extended.exceptions import JWTExtendedException
from jwt import PyJWTError

from .auth import auth
from .posts import posts


def register_routes(app):
    """Register all routes for the API."""
    app.register_blueprint(posts)
    app.register_blueprint(auth)

    @app.errorhandler(PyJWTError)
    @app.errorhandler(JWTExtendedException)
    def handle_jwt_errors(error):
        return {"message": str(error)}, 401
