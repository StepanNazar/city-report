from api.blueprints.common.routes import CustomAPIBlueprint

posts = CustomAPIBlueprint("posts", __name__, tag="Posts operations", url_prefix="/")
