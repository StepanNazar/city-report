from api.blueprints.common.routes import CustomAPIBlueprint

uploads_bp = CustomAPIBlueprint(
    "uploads", __name__, tag="Uploads operations", url_prefix="/uploads"
)
