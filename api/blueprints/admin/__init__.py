from api.blueprints.common.routes import CustomAPIBlueprint

admin = CustomAPIBlueprint("admin", __name__, tag="Admin operations", url_prefix="/")

from . import models, routes  # noqa: E402, F401
