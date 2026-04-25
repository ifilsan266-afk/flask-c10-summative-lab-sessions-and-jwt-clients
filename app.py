from flask import Flask
from flask_migrate import Migrate
from models import db, bcrypt
from auth import auth_bp
from notes import notes_bp


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///productivity.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "super-secret-key-change-in-production"

    db.init_app(app)
    bcrypt.init_app(app)
    Migrate(app, db)

    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
