from marshmallow import Schema, fields
from bson import ObjectId

Schema.TYPE_MAPPING[ObjectId] = fields.String()


class UserSchema(Schema):
    id = fields.String()
    name = fields.String()
    email = fields.Email()
    password = fields.String(load_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    deleted_at = fields.DateTime(dump_only=True)

    def load(self, data, *args, **kwargs):
        data.pop("password", None)
        return super(UserSchema, self).load(data, *args, **kwargs)

    class Meta:
        exclude = ["deleted_at", "created_at", "updated_at"]


user_schema = UserSchema()
