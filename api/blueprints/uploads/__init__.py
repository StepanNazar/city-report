from api.blueprints.common.routes import CustomAPIBlueprint

uploads = CustomAPIBlueprint(
    "uploads", __name__, tag="Uploads operations", url_prefix="/uploads"
)
from . import models, routes  # noqa: E402, F401
