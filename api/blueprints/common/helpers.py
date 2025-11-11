import requests
from apiflask import abort

from api import db
from api.services import LocationService


def get_or_create_locality(locality_id, locality_provider):
    try:
        return LocationService.get_or_create_locality(
            locality_id, locality_provider, db.session
        )
    except ValueError:
        abort(400, message="Invalid locality id")
    except requests.RequestException:
        abort(500, message="Nominatim service unavailable")
    except NotImplementedError as e:
        abort(501, message=str(e))
