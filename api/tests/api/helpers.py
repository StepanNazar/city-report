from types import MappingProxyType

from pytest_lazy_fixtures import lf as _lf

from api.tests.api.data import post_data, solution_data


def lf(fixture):
    """Converts a fixture to a lazy fixture which can be used in parametrize."""
    fixture_name = fixture.__name__
    return _lf(fixture_name)


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


def create_post_with_images(
    client, images_ids, post_data: dict | MappingProxyType = post_data
):
    """Create a post with specified images and return its URL."""
    data = dict(post_data)
    data["imagesIds"] = images_ids
    return create_post(client, data)


def create_post(client, post_data: dict | MappingProxyType = post_data):
    response = client.post("/posts", json=post_data.copy())
    return response.headers["Location"]


def create_solution(
    client, post_url: str, solution_data: dict | MappingProxyType = solution_data
):
    response = client.post(f"{post_url}/solutions", json=solution_data.copy())
    return response.headers["Location"]


def create_solution_with_images(
    client,
    post_url: str,
    images_ids,
    solution_data: dict | MappingProxyType = solution_data,
):
    """Create a solution with specified images and return its URL."""
    data = dict(solution_data)
    data["imagesIds"] = images_ids
    return create_solution(client, post_url, data)
