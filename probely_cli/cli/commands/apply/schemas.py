from marshmallow import Schema, fields, INCLUDE


class ApplyFileSchema(Schema):
    action = fields.Str(required=True)
    payload = fields.Dict(required=True)

    class META:
        unknown = INCLUDE


class SiteSchema(Schema):
    url = fields.Str(required=True)

    class META:
        unknown = INCLUDE


class AddTargetActionSchema(Schema):
    site = fields.Nested(SiteSchema, required=True)

    class META:
        unknown = INCLUDE
