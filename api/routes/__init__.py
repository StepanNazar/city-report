from flask_jwt_extended.exceptions import JWTExtendedException
from jwt import PyJWTError

from .admin import admin
from .ai_comments import ai_comments
from .auth import auth
from .comments import comments
from .posts import posts
from .solutions import solutions
from .uploads import images
from .users import users


def register_routes(app):
    """Register all routes for the API."""
    app.register_blueprint(admin)
    app.register_blueprint(ai_comments)
    app.register_blueprint(auth)
    app.register_blueprint(comments)
    app.register_blueprint(images)
    app.register_blueprint(posts)
    app.register_blueprint(solutions)
    app.register_blueprint(users)

    @app.errorhandler(PyJWTError)
    @app.errorhandler(JWTExtendedException)
    def handle_jwt_errors(error):
        return {"message": str(error)}, 401
