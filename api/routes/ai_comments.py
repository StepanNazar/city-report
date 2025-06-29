from apiflask import APIBlueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required

ai_comments = APIBlueprint(
    "ai_comments", __name__, tag="AI Comments operations", url_prefix="/"
)


class PostAIComment(MethodView):
    def get(self, post_id):
        """Get AI comment for post"""
        return {}, 501

    @jwt_required()
    @ai_comments.doc(
        security="jwt_access_token", responses={202: "AI comment generation started"}
    )
    def put(self, post_id):
        """Request generation of AI comment for post. Activated account required."""
        return {}, 501


class CityAIPrompt(MethodView):
    @jwt_required()
    @ai_comments.doc(
        security="jwt_access_token",
        responses={403: "Forbidden", 200: "AI prompt retrieved"},
    )
    def get(self, city_id):
        """Get AI prompt for city. Only for admins."""
        return {}, 501

    @jwt_required()
    @ai_comments.doc(
        security="jwt_access_token",
        responses={403: "Forbidden", 200: "AI prompt updated"},
    )
    def put(self, city_id):
        """Update AI prompt for city. Only for admins."""
        return {}, 501


class DefaultCityAIPrompt(MethodView):
    @jwt_required()
    @ai_comments.doc(
        security="jwt_access_token",
        responses={403: "Forbidden", 200: "Default AI prompt retrieved"},
    )
    def get(self):
        """Get the default AI prompt. Only for admins."""
        return {}, 501

    @jwt_required()
    @ai_comments.doc(
        security="jwt_access_token",
        responses={403: "Forbidden", 200: "Default AI prompt updated"},
    )
    def put(self):
        """Update default AI prompt. Only for admins."""
        return {}, 501


class CityAIDataSuggestions(MethodView):
    @jwt_required()
    @ai_comments.doc(
        security="jwt_access_token",
        responses={403: "Forbidden", 200: "AI data suggestions retrieved"},
    )
    def get(self, city_id):
        """Get AI data suggestions for the city. Only for admins."""
        return {}, 501

    @jwt_required()
    @ai_comments.doc(
        security="jwt_access_token", responses={201: "AI data suggestion sent"}
    )
    def post(self, city_id):
        """Send AI data suggestion for city to admins. Activated account required."""
        return {}, 501


class CityAIDataSuggestion(MethodView):
    @jwt_required()
    @ai_comments.doc(
        security="jwt_access_token",
        responses={403: "Forbidden", 200: "AI data suggestion retrieved"},
    )
    def get(self, city_id, suggestion_id):
        """Get specific AI data suggestion. Only for admins."""
        return {}, 501

    @jwt_required()
    @ai_comments.doc(
        security="jwt_access_token",
        responses={403: "Forbidden", 204: "AI data suggestion deleted"},
    )
    def delete(self, city_id, suggestion_id):
        """Delete AI data suggestion. Only for admins."""
        return {}, 501


ai_comments.add_url_rule(
    "/posts/<int:post_id>/ai-comment",
    view_func=PostAIComment.as_view("post_ai_comment"),
)
ai_comments.add_url_rule(
    "/localities/<int:city_id>/ai-prompt",
    view_func=CityAIPrompt.as_view("city_ai_prompt"),
)
ai_comments.add_url_rule(
    "/localities/default/ai-prompt",
    view_func=DefaultCityAIPrompt.as_view("default_city_ai_prompt"),
)
ai_comments.add_url_rule(
    "/localities/<int:city_id>/ai-data-suggestions",
    view_func=CityAIDataSuggestions.as_view("city_ai_data_suggestions"),
)
ai_comments.add_url_rule(
    "/localities/<int:city_id>/ai-data-suggestions/<int:suggestion_id>",
    view_func=CityAIDataSuggestion.as_view("city_ai_data_suggestion"),
)
