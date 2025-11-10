from types import MappingProxyType

import pytest
from pytest_lazy_fixtures import lf as _lf

from api import create_app
from api import db as _db
from api.config import TestConfig


@pytest.fixture(autouse=True, scope="session")
def app():
    """
    Application instantiator for each unit test session.

    1) Build the application base at the beginning of session
    2) Create database tables, yield the app for individual tests
    3) Final tear down logic at the end of the session
    """
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
    assert response.json["total_items"] == total
    assert response.json["total_pages"] == total_pages
    assert response.json["page"] == page
    assert len(response.json["items"]) == items_count


def assert_resources_order_match(returned_resources, expected_resources):
    """Verify returned resources match expected resources."""
    for i, expected_source in enumerate(expected_resources):
        for key, value in expected_source.items():
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
