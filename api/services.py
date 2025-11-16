import requests

from api.blueprints.auth.models import User
from api.blueprints.locations.models import Locality


class EmailService:  # replace with flask-mail?
    def send_email(self, receiver: str, subject: str, message: str):
        # not implemented
        print(
            f"Sending email to {receiver} with subject {subject} and message {message}"
        )

    def send_activation_link(self, user: User):
        self.send_email(
            user.email,
            "City Report: Activate your account",
            f"Hello, {user.firstname}!\n"
            f"Click the link to activate your account:"
            f"http://localhost:5000/activate/{user.activation_code}",
        )


class NominatimService:
    @staticmethod
    def get_latitude_longitude(locality_id: int) -> tuple[float, float]:
        url = "https://nominatim.openstreetmap.org/lookup?osm_ids=N{},W{},R{}&format=geocodejson"
        url = url.format(locality_id, locality_id, locality_id)
        headers = {"User-Agent": "City Report", "Accept-language": "en"}
        r = requests.get(url, timeout=10, headers=headers)
        r.raise_for_status()
        json = r.json()
        if len(json["features"]) == 0:
            raise ValueError("Invalid locality id")
        latitude = json["features"][0]["geometry"]["coordinates"][1]
        longitude = json["features"][0]["geometry"]["coordinates"][0]
        return latitude, longitude


class LocationService:
    """Service for handling locality operations across different providers."""

    @staticmethod
    def get_or_create_locality(
        locality_id: int, locality_provider: str, db_session
    ) -> Locality:
        """
        Get or create a locality based on provider and ID.

        Args:
            locality_id: The ID of the locality in the provider's system
            locality_provider: The provider name (e.g., "nominatim", "google")
            db_session: The database session to use for queries and commits

        Returns:
            Locality: The locality object

        Raises:
            ValueError: If locality_id is invalid
            requests.RequestException: If the external service is unavailable
            NotImplementedError: If the provider is not supported
        """

        if locality_provider == "nominatim":
            locality = Locality.query.filter_by(osm_id=locality_id).first()
            if not locality:
                latitude, longitude = NominatimService.get_latitude_longitude(
                    locality_id
                )
                locality = Locality(
                    osm_id=locality_id,  # type: ignore
                    latitude=latitude,  # type: ignore
                    longitude=longitude,  # type: ignore
                )
                db_session.add(locality)
                db_session.flush()
            return locality
        elif locality_provider == "google":
            raise NotImplementedError("Google location provider not yet implemented")
        else:
            raise NotImplementedError("Unsupported locality provider")
