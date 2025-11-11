from api.blueprints.common.routes import CustomAPIBlueprint

posts = CustomAPIBlueprint("posts", __name__, tag="Posts operations", url_prefix="/")
from . import models, routes  # noqa: E402, F401
