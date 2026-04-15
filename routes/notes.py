from flask import Blueprint, request, session
from models import Note
from extensions import db
from schemas import note_schema, notes_schema

notes_bp = Blueprint("notes", __name__)


def check_auth():
    return session.get("user_id")


@notes_bp.route("/notes", methods=["GET"])
def get_notes():
    user_id = check_auth()
    if not user_id:
        return {"error": "Unauthorized"}, 401

    page = request.args.get("page", 1, type=int)
    per_page = 5

    pagination = Note.query.filter_by(user_id=user_id).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return {
        "items": notes_schema.dump(pagination.items),
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page
    }, 200


@notes_bp.route("/notes", methods=["POST"])
def create_note():
    user_id = check_auth()
    if not user_id:
        return {"error": "Unauthorized"}, 401

    data = request.get_json() or {}

    note = Note(
        title=data.get("title"),
        content=data.get("content"),
        user_id=user_id
    )

    db.session.add(note)
    db.session.commit()

    return note_schema.dump(note), 201


@notes_bp.route("/notes/<int:id>", methods=["GET"])
def get_note(id):
    user_id = check_auth()
    if not user_id:
        return {"error": "Unauthorized"}, 401

    note = Note.query.get(id)

    if not note:
        return {"error": "Not found"}, 404

    if note.user_id != user_id:
        return {"error": "Forbidden"}, 403

    return note_schema.dump(note), 200


@notes_bp.route("/notes/<int:id>", methods=["PATCH"])
def update_note(id):
    user_id = check_auth()
    if not user_id:
        return {"error": "Unauthorized"}, 401

    note = Note.query.get(id)

    if not note:
        return {"error": "Not found"}, 404

    if note.user_id != user_id:
        return {"error": "Forbidden"}, 403

    data = request.get_json() or {}

    note.title = data.get("title", note.title)
    note.content = data.get("content", note.content)

    db.session.commit()

    return note_schema.dump(note), 200


@notes_bp.route("/notes/<int:id>", methods=["DELETE"])
def delete_note(id):
    user_id = check_auth()
    if not user_id:
        return {"error": "Unauthorized"}, 401

    note = Note.query.get(id)

    if not note:
        return {"error": "Not found"}, 404

    if note.user_id != user_id:
        return {"error": "Forbidden"}, 403

    db.session.delete(note)
    db.session.commit()

    return {"message": "Deleted"}, 200