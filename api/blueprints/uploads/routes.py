from apiflask import FileSchema
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from api.blueprints.uploads import uploads
from api.blueprints.uploads.schemas import ImageLinkOutSchema, ImageSchema


class Images(MethodView):
    @jwt_required()
    @uploads.input(ImageSchema, location="files")
    @uploads.output(ImageLinkOutSchema, status_code=201)
    @uploads.doc(security="jwt_access_token", responses={201: "Image uploaded"})
    def post(self):
        """Upload image. Activated account required."""
        return {}, 501


class Image(MethodView):
    @uploads.output(FileSchema, content_type="image")
    def get(self, image_id):
        """Get image by ID"""
        return {}, 501


uploads.add_url_rule("/images", view_func=Images.as_view("images"))
uploads.add_url_rule("/images/<uuid:image_id>", view_func=Image.as_view("image"))
