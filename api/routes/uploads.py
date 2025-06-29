from apiflask import APIBlueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required

images = APIBlueprint(
    "uploads", __name__, tag="Uploads operations", url_prefix="/uploads"
)


class Images(MethodView):
    @jwt_required()
    @images.doc(security="jwt_access_token", responses={201: "Image uploaded"})
    def post(self):
        """Upload image. Activated account required."""
        return {}, 501


class Image(MethodView):
    def get(self, image_id):
        """Get image by ID"""
        return {}, 501


images.add_url_rule("/images", view_func=Images.as_view("images"))
images.add_url_rule("/images/<uuid:image_id>", view_func=Image.as_view("image"))
