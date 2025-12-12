from api.blueprints.common.routes import CustomAPIBlueprint

auth = CustomAPIBlueprint(
    "auth", __name__, tag="Authentication operations", url_prefix="/auth"
)
