from marshmallow import Schema, fields

class NoteSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)

note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)