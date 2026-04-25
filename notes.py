from flask import Blueprint, request, jsonify, session
from models import db, Note
from schemas import NoteSchema

notes_bp = Blueprint("notes", __name__)
note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)


def get_current_user_id():
    return session.get("user_id")


@notes_bp.route("/notes", methods=["GET"])
def get_notes():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    # Pagination
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    paginated = Note.query.filter_by(user_id=user_id).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        "notes": notes_schema.dump(paginated.items),
        "total": paginated.total,
        "pages": paginated.pages,
        "current_page": paginated.page
    }), 200


@notes_bp.route("/notes", methods=["POST"])
def create_note():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}
    errors = note_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        note = Note(
            title=data["title"],
            content=data["content"],
            category=data.get("category", "general"),
            user_id=user_id
        )
        db.session.add(note)
        db.session.commit()
        return jsonify(note_schema.dump(note)), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@notes_bp.route("/notes/<int:id>", methods=["GET"])
def get_note(id):
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    note = db.session.get(Note, id)
    if not note:
        return jsonify({"error": "Note not found"}), 404

    # Users can only access their own notes
    if note.user_id != user_id:
        return jsonify({"error": "Forbidden"}), 403

    return jsonify(note_schema.dump(note)), 200


@notes_bp.route("/notes/<int:id>", methods=["PATCH"])
def update_note(id):
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    note = db.session.get(Note, id)
    if not note:
        return jsonify({"error": "Note not found"}), 404

    if note.user_id != user_id:
        return jsonify({"error": "Forbidden"}), 403

    data = request.get_json() or {}
    try:
        if "title" in data:
            note.title = data["title"]
        if "content" in data:
            note.content = data["content"]
        if "category" in data:
            note.category = data["category"]
        db.session.commit()
        return jsonify(note_schema.dump(note)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@notes_bp.route("/notes/<int:id>", methods=["DELETE"])
def delete_note(id):
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    note = db.session.get(Note, id)
    if not note:
        return jsonify({"error": "Note not found"}), 404

    if note.user_id != user_id:
        return jsonify({"error": "Forbidden"}), 403

    db.session.delete(note)
    db.session.commit()
    return {}, 204
