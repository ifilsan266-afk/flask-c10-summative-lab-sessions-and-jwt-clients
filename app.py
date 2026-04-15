from flask import Flask
from config import Config
from extensions import db, bcrypt
from flask_migrate import Migrate

from routes.auth import auth_bp
from routes.notes import notes_bp

app = Flask(__name__)
app.config.from_object(Config)

# initialize extensions
db.init_app(app)
bcrypt.init_app(app)
migrate = Migrate(app, db)

# register blueprints (clean structure)
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(notes_bp, url_prefix="/api")

# health check route
@app.route("/")
def home():
    return {
        "message": "API is running",
        "status": "success"
    }, 200


if __name__ == "__main__":
    app.run(debug=True)