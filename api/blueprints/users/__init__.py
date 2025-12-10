from api.blueprints.common.routes import CustomAPIBlueprint

users = CustomAPIBlueprint("users", __name__, tag="Users operations", url_prefix="/")
