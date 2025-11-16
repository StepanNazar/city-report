from api.blueprints.common.routes import CustomAPIBlueprint

comments = CustomAPIBlueprint(
    "comments", __name__, tag="Comments operations", url_prefix="/"
)
