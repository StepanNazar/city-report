from apiflask import Schema
from apiflask.fields import URL, UUID, File
from apiflask.validators import FileSize, FileType


class ImageSchema(Schema):
    image = File(
        validate=[FileType([".png", ".jpg", ".jpeg", ".gif"]), FileSize(max="5 MB")],
        required=True,
    )


class ImageLinkOutSchema(Schema):
    id = UUID()
    url = URL(metadata={"x-faker": "image.url"})
