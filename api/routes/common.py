import typing as t

from apiflask import APIBlueprint
from apiflask.types import DecoratedType

from api.schemas.common import LocationHeader


class CustomAPIBlueprint(APIBlueprint):
    def output(self, *args, **kwargs) -> t.Callable[[DecoratedType], DecoratedType]:
        if kwargs.get("status_code") == 201 and kwargs.get("headers") is None:
            kwargs["headers"] = LocationHeader
        return super().output(*args, **kwargs)
