from apiflask import FileSchema
from apiflask.views import MethodView
from flask_jwt_extended import jwt_required

from api import db, get_app
from api.blueprints.uploads import uploads_bp
from api.blueprints.uploads.schemas import ImageLinkOutSchema, ImageSchema
from api.blueprints.uploads.services import StorageService


class Images(MethodView):
    @jwt_required()
    @uploads_bp.input(ImageSchema, location="files")
    @uploads_bp.output(ImageLinkOutSchema, status_code=201)
    @uploads_bp.doc(security="jwt_access_token", responses={201: "Image uploaded"})
    def post(self, files_data):
        """Upload image. Activated account required."""
        storage: StorageService = get_app().storage_service
        image = storage.upload_image(files_data["image"], db.session)
        return image, 201, {"Location": image.url}


class Image(MethodView):
    @uploads_bp.output(FileSchema, content_type="image")
    def get(self, filename):
        """Get image by ID"""
        return get_app().storage_service.send_file(filename)


uploads_bp.add_url_rule("/images", view_func=Images.as_view("images"))
uploads_bp.add_url_rule("/images/<string:filename>", view_func=Image.as_view("image"))
