from apiflask import Schema
from apiflask.fields import DateTime, Integer, String


class PostSchema(Schema):
    id = Integer()
    authorID = Integer()
    authorName = String(metadata={"x-faker": "name.firstName"})
    creationTime = DateTime(metadata={"x-faker": "date.recent"})
    latitude = String(metadata={"x-faker": "address.latitude"})
    longitude = String(metadata={"x-faker": "address.longitude"})
    country = String(metadata={"x-faker": "address.country"})
    state = String(metadata={"x-faker": "address.state"})
    locality = String(metadata={"x-faker": "address.city"})
    title = String(metadata={"x-faker": "lorem.sentences"})
    body = String(metadata={"x-faker": "lorem.paragraphs"})
