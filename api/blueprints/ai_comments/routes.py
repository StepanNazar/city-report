from flask.views import MethodView
from flask_jwt_extended import jwt_required

from api.blueprints.ai_comments import ai_comments
from api.blueprints.ai_comments.schemas import (
    AICommentSchema,
    AIDataSuggestionPaginationSchema,
    AIDataSuggestionSchema,
    AIDataSuggestionSortingSchema,
    AIPromptSchema,
    APIKeySchema,
    LocalityIDListSchema,
)
from api.blueprints.common.schemas import (
    TextBodySchema,
    merge_schemas,
    pagination_query_schema,
)


class PostAIComment(MethodView):
    @ai_comments.output(AICommentSchema)
    def get(self, post_id):
        """Get AI comment for post"""
        return {}, 501

    @jwt_required()
    @ai_comments.input(APIKeySchema)
    @ai_comments.doc(
        security="jwt_access_token",
        responses={
            202: "AI comment generation started",
            200: "AI comment already exists",
            409: "AI comment generation already in progress",
        },
    )
    def put(self, post_id):
        """Request generation of AI comment for post. Activated account required."""
        return {}, 501


class LocalityAIPrompt(MethodView):
    @jwt_required()
    @ai_comments.output(AIPromptSchema)
    @ai_comments.doc(
        security="jwt_access_token",
        responses={403: "Forbidden", 200: "AI prompt retrieved"},
    )
    def get(self, city_id):
        """Get AI prompt for city. Only for admins."""
        return {}, 501

    @jwt_required()
    @ai_comments.input(AIPromptSchema)
    @ai_comments.doc(
        security="jwt_access_token",
        responses={403: "Forbidden", 200: "AI prompt updated"},
    )
    def put(self, city_id):
        """Update AI prompt for city. Only for admins."""
        return {}, 501


class DefaultLocalityAIPrompt(MethodView):
    @jwt_required()
    @ai_comments.output(AIPromptSchema)
    @ai_comments.doc(
        security="jwt_access_token",
        responses={403: "Forbidden", 200: "Default AI prompt retrieved"},
    )
    def get(self):
        """Get the default AI prompt. Only for admins."""
        return {}, 501

    @jwt_required()
    @ai_comments.input(AIPromptSchema)
    @ai_comments.doc(
        security="jwt_access_token",
        responses={403: "Forbidden", 200: "Default AI prompt updated"},
    )
    def put(self):
        """Update default AI prompt. Only for admins."""
        return {}, 501


class LocalitiesWithAIDataSuggestions(MethodView):
    @jwt_required()
    @ai_comments.output(LocalityIDListSchema)
    @ai_comments.doc(
        security="jwt_access_token",
        responses={
            403: "Forbidden",
            200: "Localities with AI data suggestions retrieved",
        },
    )
    def get(self):
        """Get localities with AI data suggestions. Only for admins."""
        return {}, 501


class LocalityAIDataSuggestions(MethodView):
    @jwt_required()
    @ai_comments.input(
        merge_schemas(pagination_query_schema(), AIDataSuggestionSortingSchema),
        location="query",
    )
    @ai_comments.output(AIDataSuggestionPaginationSchema)
    @ai_comments.doc(
        security="jwt_access_token",
        responses={403: "Forbidden", 200: "AI data suggestions retrieved"},
    )
    def get(self, city_id, query_data):
        """Get AI data suggestions for the city. Only for admins. Ordered by creation date."""
        return {}, 501

    @jwt_required()
    @ai_comments.input(TextBodySchema)
    @ai_comments.doc(
        security="jwt_access_token", responses={204: "AI data suggestion sent"}
    )
    def post(self, city_id):
        """Send AI data suggestion for city to admins. Activated account required."""
        return {}, 501


class LocalityAIDataSuggestion(MethodView):
    @jwt_required()
    @ai_comments.output(AIDataSuggestionSchema)
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
    "/localities/<int:locality_id>/ai-prompt",
    view_func=LocalityAIPrompt.as_view("city_ai_prompt"),
)
ai_comments.add_url_rule(
    "/localities/default/ai-prompt",
    view_func=DefaultLocalityAIPrompt.as_view("default_city_ai_prompt"),
)
ai_comments.add_url_rule(
    "/localities/with-suggestions",
    view_func=LocalitiesWithAIDataSuggestions.as_view("localities_with_ai_suggestions"),
)
ai_comments.add_url_rule(
    "/localities/<int:locality_id>/ai-data-suggestions",
    view_func=LocalityAIDataSuggestions.as_view("city_ai_data_suggestions"),
)
ai_comments.add_url_rule(
    "/localities/<int:locality_id>/ai-data-suggestions/<int:suggestion_id>",
    view_func=LocalityAIDataSuggestion.as_view("city_ai_data_suggestion"),
)
