from api.blueprints.common.routes import CustomAPIBlueprint

locations = CustomAPIBlueprint(
    "locations", __name__, tag="Locations operations", url_prefix="/"
)
