from api.blueprints.common.routes import CustomAPIBlueprint

solutions = CustomAPIBlueprint(
    "solutions", __name__, tag="Solutions operations", url_prefix="/"
)
