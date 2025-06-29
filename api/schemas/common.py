from apiflask import Schema


def snake_to_camel(string):
    parts = string.split("_")
    return parts[0] + "".join(p.title() for p in parts[1:])


class CamelCaseSchema(Schema):
    """Base schema that auto converts snake_case ⇄ camelCase"""

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = snake_to_camel(field_name)
