from types import MappingProxyType

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
additional_post_keys = [  # additional keys that should be present in post's output schema, but not in the input schema
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
