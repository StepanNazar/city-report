from api.models import User


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
