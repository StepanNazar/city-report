from .auth import auth
from .posts import posts
from api import api

api.add_namespace(posts)
api.add_namespace(auth)
