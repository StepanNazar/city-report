from apiflask import Schema
from apiflask.fields import Boolean, DateTime, Integer, String
from apiflask.validators import Length, OneOf

from api.blueprints.common.schemas import CamelCaseSchema, pagination_schema


class UserOutSchema(CamelCaseSchema):
    id = Integer()
    first_name = String(metadata={"x-faker": "name.firstName"})
    last_name = String(metadata={"x-faker": "name.lastName"})
    email = String(metadata={"x-faker": "internet.email"})
    country = String(metadata={"x-faker": "address.country"})
    state = String(metadata={"x-faker": "address.state"})
    locality = String(metadata={"x-faker": "address.city"})
    country_id = Integer()
    state_id = Integer()
    locality_id = Integer()
    created_at = DateTime(metadata={"x-faker": "date.past"})
    updated_at = DateTime(metadata={"x-faker": "date.recent"})
    profile_description = String(metadata={"x-faker": "lorem.paragraphs"})
    posts = Integer()
    solutions = Integer()
    comments = Integer()
    liked_posts = Integer()
    disliked_posts = Integer()
    liked_solutions = Integer()
    disliked_solutions = Integer()
    liked_comments = Integer()
    disliked_comments = Integer()
    is_banned = Boolean()
    is_admin = Boolean()


UserOutPaginationSchema = pagination_schema(
    UserOutSchema, exclude=["profile_description"]
)


class ReactionSchema(CamelCaseSchema):
    """Schema for reaction input"""

    reaction = String(required=True, validate=OneOf(["like", "dislike"]))


class UserReactionOutSchema(ReactionSchema):
    related_type = String(validate=OneOf(["comment", "solution", "post"]))
    related_id = Integer()
    related_title = String(metadata={"x-faker": "lorem.sentence"})
    related_author_id = Integer()
    related_author_first_name = String(metadata={"x-faker": "name.firstName"})
    reaction_time = DateTime(metadata={"x-faker": "date.past"})


UserReactionOutPaginationSchema = pagination_schema(UserReactionOutSchema)


class UserReactionSortingFilteringSchema(Schema):
    order = String(
        load_default="desc",
        validate=OneOf(["asc", "desc"]),
    )
    related_type = String(validate=OneOf(["post", "solution", "comment"]))


class UserBanPatchSchema(CamelCaseSchema):
    reason = String(
        required=True,
        validate=Length(max=500),
        metadata={"x-faker": "lorem.paragraph"},
    )
    expires_at = DateTime(
        required=True,
        metadata={"x-faker": "date.future"},
    )


class UserBanInSchema(UserBanPatchSchema):
    user_id = Integer()


class UserBanOutSchema(UserBanInSchema):
    id = Integer()
    user_email = String(metadata={"x-faker": "internet.email"})
    user_first_name = String(metadata={"x-faker": "name.firstName"})
    user_last_name = String(metadata={"x-faker": "name.lastName"})
    created_at = DateTime(metadata={"x-faker": "date.past"})
    updated_at = DateTime(metadata={"x-faker": "date.recent"})


UserBanOutPaginationSchema = pagination_schema(UserBanOutSchema, exclude=["reason"])


class UserBanSortingFilteringSchema(Schema):
    sort_by = String(
        load_default="expires_at",
        validate=OneOf(["created_at", "updated_at", "expires_at"]),
    )
    order = String(
        load_default="desc",
        validate=OneOf(["asc", "desc"]),
    )
    min_created_at = DateTime()
    max_created_at = DateTime()
    min_updated_at = DateTime()
    max_updated_at = DateTime()
    min_expires_at = DateTime()
    max_expires_at = DateTime()
