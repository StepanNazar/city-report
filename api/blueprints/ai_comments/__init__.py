from api.blueprints.common.routes import CustomAPIBlueprint

ai_comments = CustomAPIBlueprint(
    "ai_comments", __name__, tag="AI Comments operations", url_prefix="/"
)
