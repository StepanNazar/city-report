from apiflask import APIBlueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required

users = APIBlueprint("users", __name__, tag="Users operations", url_prefix="/")


class User(MethodView):
    def get(self, user_id):
        """Get user profile"""
        return {}, 501


class UserPosts(MethodView):
    def get(self, user_id):
        """Get user posts"""
        return {}, 501


class UserSolutions(MethodView):
    def get(self, user_id):
        """Get user solutions"""
        return {}, 501


class UserComments(MethodView):
    def get(self, user_id):
        """Get user comments"""
        return {}, 501


class UserReactions(MethodView):
    def get(self, user_id):
        """Get user reactions"""
        return {}, 501


class UserMe(MethodView):
    @jwt_required()
    @users.doc(security="jwt_access_token")
    def patch(self):
        """Edit the current user profile using JSON Patch."""
        return {}, 501


class UserBans(MethodView):
    @jwt_required()
    @users.doc(
        security="jwt_access_token",
        responses={200: "User bans retrieved", 403: "Forbidden"},
    )
    def get(self, user_id):
        """Get user's bans. Only for admins and the user themselves."""
        return {}, 501

    @jwt_required()
    @users.doc(
        security="jwt_access_token",
        responses={201: "User ban created", 403: "Forbidden"},
    )
    def post(self, user_id):
        """Create a user's ban. Only for admins."""
        return {}, 501


class UserBan(MethodView):
    @jwt_required()
    @users.doc(
        security="jwt_access_token",
        responses={204: "User ban retrieved", 403: "Forbidden"},
    )
    def get(self, user_id, ban_id):
        """Get the specific user's ban. Only for admins and the user themselves."""
        return {}, 501

    @jwt_required()
    @users.doc(
        security="jwt_access_token",
        responses={204: "User ban deleted", 403: "Forbidden"},
    )
    def patch(self, user_id, ban_id):
        """Partially update the user's ban. Only for admins."""
        return {}, 501


users.add_url_rule("/users/<int:user_id>", view_func=User.as_view("user"))
users.add_url_rule(
    "/users/<int:user_id>/posts", view_func=UserPosts.as_view("user_posts")
)
users.add_url_rule(
    "/users/<int:user_id>/solutions", view_func=UserSolutions.as_view("user_solutions")
)
users.add_url_rule(
    "/users/<int:user_id>/comments", view_func=UserComments.as_view("user_comments")
)
users.add_url_rule(
    "/users/<int:user_id>/reactions", view_func=UserReactions.as_view("user_reactions")
)
users.add_url_rule("/users/me", view_func=UserMe.as_view("user_me"))
users.add_url_rule("/users/<int:user_id>/bans", view_func=UserBans.as_view("user_bans"))
users.add_url_rule(
    "/users/<int:user_id>/bans/<int:ban_id>", view_func=UserBan.as_view("user_ban")
)
