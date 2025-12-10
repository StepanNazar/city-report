# City Report API - Gemini AI Configuration

This file contains rules and guidelines for developing the Python/Flask backend.

## 1. Technology Stack & Key Files

- **Framework:** Flask and APIFlask
- **Database:** SQLAlchemy (ORM)
- **Migrations:** Flask-Migrate (using Alembic)
- **Testing:** Pytest
- **Linting/Formatting:** Ruff (configured in `pyproject.toml`)
- **Type Checking:** Pyright (configured in `pyrightconfig.json`)
- **API Specification:** OpenAPI (generated from code into `openapi.json`)

## 2. Backend Architecture

The API is organized into modules using Flask Blueprints. This structure is designed to be modular and scalable.

- **Blueprints (`api/blueprints/`):**
  - Each directory inside `blueprints` is a self-contained module (e.g., `posts`, `users`, `auth`).
  - A typical blueprint contains:
    - `__init__.py`: Registers the blueprint with the Flask app.
    - `models.py`: Defines the SQLAlchemy database models for that resource.
    - `routes.py`: Defines the API endpoints (e.g., `@bp.get('/posts')`).
    - `schemas.py`: Defines the APIFlask (Marshmallow) schemas for data validation and serialization.
- **Common Logic (`api/blueprints/common/`):**
  - This special directory contains reusable code (models, helper functions, schemas) that is shared across multiple blueprints. **DRY Principle:** Before writing new code, check if similar functionality exists here.
- **Entry Point (`dev.py`):** This is the main file to run the application for development.
- **Configuration (`config.py`):** All application configuration (secret keys, database URIs, etc.) is managed here.

## 3. Python & Flask Best Practices

- **Styling:** All code **MUST** follow **PEP 8** standards. Use `ruff` to format and lint your code.
- **Type Hinting:** All functions and methods **MUST** have full type hints. The project uses `pyright` for strict type checking.
- **Flask Blueprints:** All new features must be organized within an existing or new blueprint.
- **Database Models:** When you modify a `models.py` file, you **MUST** also generate a new database migration using `flask db migrate` and `flask db upgrade`. **Important:** Alembic can sometimes generate incorrect migration files; always review them carefully and fix if needed.
- **Error Handling:** Use standard Flask error handling. Do not return generic 500 errors; use specific HTTP status codes and error messages.

## 4. Testing Conventions

The testing strategy is comprehensive and **MUST** be followed.

- **Location:** All tests are located in `api/tests/api/`.
- **Fixtures (`conftest.py`):** Common test setup (like creating an app client, initializing the database, or creating test users) is handled by pytest fixtures in `conftest.py`. Use these fixtures to keep tests clean.
- **Helpers & Data (`helpers.py`, `data.py`):** Use these files for reusable test functions and static test data.
- **Test Structure:**
  - For endpoints specific to one resource (e.g., a special action on a post), add the test to the corresponding file (e.g., `test_posts.py`).
  - For general CRUD operations or cross-resource tests, use the parameterized test files:
    - `test_resources_crud.py`: For testing basic Create, Read, Update, Delete operations.
    - `test_resources_with_images.py`: For testing resources that involve image uploads.
    - `test_unauthorized_access.py`: For testing permission and authorization rules.
- **TDD Requirement:** All new features or bug fixes **MUST** be accompanied by tests that verify the change, following the TDD workflow outlined in the root `GEMINI.md`.
