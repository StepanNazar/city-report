import uuid
from types import MappingProxyType
from typing import Any

import email_validator
import pytest
from flask import Response, url_for
from pytest_lazy_fixtures import lf as _lf
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from api import create_app
from api import db as _db
from api.blueprints.uploads.services import StorageService
from api.config import TestConfig


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


def lf(fixture):
    """Converts a fixture to a lazy fixture which can be used in parametrize."""
    fixture_name = fixture.__name__
    return _lf(fixture_name)


def assert_pagination_response(response, total, page, total_pages, items_count):
    """Verify pagination metadata."""
    assert response.status_code == 200
    assert "items" in response.json
    assert response.json["totalItems"] == total
    assert response.json["totalPages"] == total_pages
    assert response.json["page"] == page
    assert len(response.json["items"]) == items_count


def assert_resources_order_match(returned_resources, expected_resources):
    """Verify returned resources match expected resources in the correct pagination order.

    This helper checks that resources are returned in the expected order by comparing
    each field in the expected resources with the corresponding field in the returned
    resources. Only fields present in both the expected and returned resources are compared,
    allowing for fields that may be excluded in pagination responses (like 'body').
    """
    for i, expected_source in enumerate(expected_resources):
        for key, value in expected_source.items():
            if key in returned_resources[i]:
                assert returned_resources[i][key] == value


def assert_response_matches_resource(
    response, resource_data, additional_keys=None, excluded_keys=None
):
    """Asserts that the response matches the resource data and has additional keys."""
    excluded_keys = excluded_keys or []
    for key, value in resource_data.items():
        if key not in excluded_keys:
            assert response.json[key] == value
    if additional_keys:
        for key in additional_keys:
            assert key in response.json


post_data = MappingProxyType(  # immutable dict view to ensure test isolation
    {
        "title": "Test Post",
        "body": "This is a test post",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "localityId": 3167397,
        "localityProvider": "nominatim",
    }
)
updated_post_data = MappingProxyType(
    {
        "title": "Updated Post",
        "body": "This is a updated test post",
        "latitude": 41.7128,
        "longitude": -73.0060,
        "localityId": 3167397,
        "localityProvider": "nominatim",
    }
)
additional_post_keys = [  # additional keys which should be present in post's output schema
    "id",
    "createdAt",
    "updatedAt",
    "authorLink",
    "authorFirstName",
    "authorLastName",
    "localityNominatimId",
    "likes",
    "dislikes",
    "comments",
]
excluded_post_keys = [  # keys present in post's input schema, but not present in the output schema
    "localityId",
    "localityProvider",
]


def upload_image(
    client, filename="test.png", content=b"fake image content"
) -> tuple[str, str]:
    """Helper function to upload an image and return its ID and URL."""
    from io import BytesIO

    data = {"image": (BytesIO(content), filename)}
    response = client.post(
        "/uploads/images", data=data, content_type="multipart/form-data"
    )
    return response.json["id"], response.json["url"]


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


def create_post_with_images(
    client, images_ids, post_data: dict | MappingProxyType = post_data
):
    """Create a post with specified images and return its URL."""
    data = dict(post_data)
    data["imagesIds"] = images_ids
    return create_post(client, data)


@pytest.fixture
def post_with_images(authenticated_client, images):
    """Create a post with 3 test images and return its URL."""
    images_ids = [img_id for img_id, _ in images]
    return create_post_with_images(authenticated_client, images_ids)


def assert_resource_images(
    response, expected_images: list[tuple[str, str] | dict[str, Any]]
):
    """Assert that response contains expected image objects {id, url} in correct order.

    Args:
        response: Flask response object
        expected_images: List of tuples (id, url) or list of dicts with 'id' and 'url' keys
    """
    assert "images" in response.json
    assert len(response.json["images"]) == len(expected_images)

    for i, expected in enumerate(expected_images):
        actual_image = response.json["images"][i]
        assert "id" in actual_image
        assert "url" in actual_image

        if isinstance(expected, tuple):
            expected_id, expected_url = expected
        else:
            expected_id, expected_url = expected["id"], expected["url"]

        assert actual_image["id"] == expected_id
        assert actual_image["url"] == expected_url


solution_data = MappingProxyType(
    {
        "title": "Test Solution",
        "body": "This is a test solution",
    }
)
updated_solution_data = MappingProxyType(
    {
        "title": "Updated Solution",
        "body": "This is a updated test solution",
    }
)
additional_solution_keys = [
    "id",
    "createdAt",
    "updatedAt",
    "authorLink",
    "authorFirstName",
    "authorLastName",
    "likes",
    "dislikes",
    "comments",
]


def create_post(client, post_data: dict | MappingProxyType = post_data):
    response = client.post("/posts", json=post_data.copy())
    return response.headers["Location"]


@pytest.fixture
def post(authenticated_client):
    """Sets up a test case with a post with post_data. Returns the post's url."""
    return create_post(authenticated_client)


def create_solution(
    client, post_url: str, solution_data: dict | MappingProxyType = solution_data
):
    response = client.post(f"{post_url}/solutions", json=solution_data.copy())
    return response.headers["Location"]


@pytest.fixture
def solution(authenticated_client, post):
    """Sets up a test case with a solution with solution_data. Returns the solution's url."""
    return create_solution(authenticated_client, post)


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


class TestStorageService(StorageService):
    def __init__(self):
        self.uploaded_images = {}

    def _upload(self, file: FileStorage) -> str:
        """Upload a file to a local folder and return its URL"""
        filename = uuid.uuid4().hex + secure_filename(file.filename or "")
        self.uploaded_images[filename] = file.read()
        return url_for("uploads.image", filename=filename)

    def send_file(self, filename: str):
        image_data = self.uploaded_images[filename]
        return Response(image_data, mimetype="image/jpeg")

    @staticmethod
    def _check_file_is_image(file: FileStorage) -> bool:
        return True
