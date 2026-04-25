from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import validates

db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    _password_hash = db.Column(db.String(200), nullable=False)

    notes = db.relationship("Note", back_populates="user", cascade="all, delete")

    @validates("username")
    def validate_username(self, key, value):
        if not value or len(value.strip()) < 3:
            raise ValueError("Username must be at least 3 characters")
        return value

    @property
    def password_hash(self):
        raise AttributeError("Password is not readable")

    @password_hash.setter
    def password_hash(self, password):
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters")
        self._password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)


class Note(db.Model):
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False, default="general")
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="notes")

    @validates("title")
    def validate_title(self, key, value):
        if not value or len(value.strip()) < 1:
            raise ValueError("Title is required")
        return value

    @validates("content")
    def validate_content(self, key, value):
        if not value or len(value.strip()) < 1:
            raise ValueError("Content is required")
        return value
