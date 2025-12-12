import email_validator
import pytest
from flask import Response
from werkzeug.datastructures import FileStorage

from api import create_app
from api import db as _db
from api.blueprints.uploads.services import LocalFolderStorageService
from api.config import TestConfig
from api.tests.api.helpers import (
    create_post,
    create_post_with_images,
    create_solution,
    create_solution_with_images,
    upload_image,
)


@pytest.fixture(autouse=True, scope="session")
def app():
    """
    Application instantiator for each unit test session.

    1) Build the application base at the beginning of session
    2) Create database tables, yield the app for individual tests
    3) Final tear down logic at the end of the session
    """
    TestConfig.STORAGE_SERVICE = TestStorageService()
    app = create_app(TestConfig)

    with app.app_context():
        _db.create_all()

        yield app

        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def db(app):
    """Database fixture with table truncation after each test."""
    yield _db

    for table in reversed(_db.metadata.sorted_tables):
        _db.session.execute(table.delete())
    _db.session.expunge_all()
    _db.session.commit()


@pytest.fixture
def client(app, db):
    """A test client for the app. Truncates tables after each test."""
    return app.test_client()


class AuthenticatedClient:
    def __init__(self, client, first_name, last_name, email, password):
        self.client = client
        response = client.post(
            "/auth/register",
            json={
                "firstName": first_name,
                "lastName": last_name,
                "email": email,
                "password": password,
            },
        )
        self.access_token = response.json["access_token"]

    def add_auth_header(self, kwargs):
        headers = kwargs.get("headers", {})
        headers["Authorization"] = f"Bearer {self.access_token}"
        kwargs["headers"] = headers

    def get(self, *args, **kwargs):
        self.add_auth_header(kwargs)
        return self.client.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        self.add_auth_header(kwargs)
        return self.client.post(*args, **kwargs)

    def put(self, *args, **kwargs):
        self.add_auth_header(kwargs)
        return self.client.put(*args, **kwargs)

    def patch(self, *args, **kwargs):
        self.add_auth_header(kwargs)
        return self.client.patch(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.add_auth_header(kwargs)
        return self.client.delete(*args, **kwargs)


@pytest.fixture
def authenticated_client(client) -> AuthenticatedClient:
    return AuthenticatedClient(
        client,
        first_name="John",
        last_name="Doe",
        email="john.doe@test.com",
        password="SecurePassw0rd!",  # noqa: S106
    )


@pytest.fixture
def authenticated_client2(client) -> AuthenticatedClient:
    return AuthenticatedClient(
        client,
        first_name="Test",
        last_name="User",
        email="test.user@test.com",
        password="TestPassw0rd!",  # noqa: S106
    )


@pytest.fixture
def image(authenticated_client) -> tuple[str, str]:
    """Upload a single test image and return its ID and URL."""
    return upload_image(authenticated_client)


@pytest.fixture
def images(authenticated_client) -> list[tuple[str, str]]:
    """Upload multiple test images and return list of tuples (id, url)."""
    return [
        upload_image(authenticated_client, f"test{i}.png", f"image {i}".encode())
        for i in range(3)
    ]


@pytest.fixture
def post_with_images(authenticated_client, images):
    """Create a post with 3 test images and return its URL."""
    images_ids = [img_id for img_id, _ in images]
    return create_post_with_images(authenticated_client, images_ids)


@pytest.fixture
def post(authenticated_client):
    """Sets up a test case with a post with post_data. Returns the post's url."""
    return create_post(authenticated_client)


@pytest.fixture
def solution(authenticated_client, post):
    """Sets up a test case with a solution with solution_data. Returns the solution's url."""
    return create_solution(authenticated_client, post)


@pytest.fixture
def solution_with_images(authenticated_client, post, images):
    """Create a solution with 3 test images and return its URL."""
    images_ids = [img_id for img_id, _ in images]
    return create_solution_with_images(authenticated_client, post, images_ids)


@pytest.fixture(autouse=True)
def mock_nominatim(mocker):
    """Mock NominatimService for tests."""
    return mocker.patch(
        "api.services.NominatimService.get_latitude_longitude",
        return_value=(40.7128, -74.0060),
    )


@pytest.fixture(autouse=True, scope="session")
def specify_testing_environment_for_email_validator():
    email_validator.TEST_ENVIRONMENT = True


class TestStorageService(LocalFolderStorageService):
    def __init__(self):
        self.uploaded_images = {}

    def _save_file(self, file: FileStorage, filename: str):
        self.uploaded_images[filename] = file.read()

    def send_file(self, filename: str):
        try:
            image_data = self.uploaded_images[filename]
        except KeyError as e:
            raise FileNotFoundError(f"File {filename} not found") from e
        return Response(image_data, mimetype="image/jpeg")

    @staticmethod
    def _check_file_is_image(file: FileStorage) -> bool:
        result = file.read() != b"not an image"
        file.seek(0)
        return result

    def _delete_file(self, filename: str):
        self.uploaded_images.pop(filename, None)


@pytest.fixture(autouse=True)
def clear_test_storage(app):
    app.storage_service.uploaded_images = {}
