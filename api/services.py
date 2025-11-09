import requests

from api.blueprints.auth.models import User


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
    def get_locality_name_state_and_country(locality_id: int) -> tuple[str, str, str]:
        url = "https://nominatim.openstreetmap.org/lookup?osm_ids=N{},W{},R{}&format=geocodejson"
        url = url.format(locality_id, locality_id, locality_id)
        headers = {"User-Agent": "City Report", "Accept-language": "en"}
        r = requests.get(url, timeout=10, headers=headers)
        r.raise_for_status()
        json = r.json()
        if len(json["features"]) == 0:
            raise ValueError("Invalid locality id")
        name = json["features"][0]["properties"]["geocoding"]["name"]
        state = json["features"][0]["properties"]["geocoding"]["state"]
        country = json["features"][0]["properties"]["geocoding"]["country"]
        return name, state, country
