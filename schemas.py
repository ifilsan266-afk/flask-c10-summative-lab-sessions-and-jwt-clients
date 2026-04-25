from marshmallow import Schema, fields, validate, validates, ValidationError


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3))


class NoteSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1))
    content = fields.Str(required=True, validate=validate.Length(min=1))
    category = fields.Str(load_default="general")
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    user_id = fields.Int(dump_only=True)

    @validates("category")
    def validate_category(self, value):
        allowed = ["general", "work", "personal", "health", "finance"]
        if value.lower() not in allowed:
            raise ValidationError(f"Category must be one of: {', '.join(allowed)}")
