from api.blueprints.common.routes import CustomAPIBlueprint

locations = CustomAPIBlueprint(
    "locations", __name__, tag="Locations operations", url_prefix="/"
)
from . import models, routes  # noqa: E402, F401
