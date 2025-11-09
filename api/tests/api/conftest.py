import pytest

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
