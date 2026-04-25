from flask import Blueprint, request, jsonify, session
from models import db, User
from schemas import UserSchema

auth_bp = Blueprint("auth", __name__)
user_schema = UserSchema()


@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json() or {}

    if not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username and password are required"}), 400

    # Check if username already taken
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already taken"}), 422

    try:
        user = User(username=data["username"])
        user.password_hash = data["password"]
        db.session.add(user)
        db.session.commit()
        session["user_id"] = user.id
        return jsonify(user_schema.dump(user)), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    user = User.query.filter_by(username=data.get("username")).first()

    if not user or not user.authenticate(data.get("password", "")):
        return jsonify({"error": "Invalid username or password"}), 401

    session["user_id"] = user.id
    return jsonify(user_schema.dump(user)), 200


@auth_bp.route("/logout", methods=["DELETE"])
def logout():
    session.pop("user_id", None)
    return {}, 204


@auth_bp.route("/me", methods=["GET"])
def me():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user_schema.dump(user)), 200
