from pathlib import Path

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    # Create a Flask instance
    app = Flask(__name__)

    # Config for the app
    app.config.from_mapping(
        SECRET_KEY="xyz",
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{Path(__file__).parent.parent / 'local.sqlite'}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # Connect SQLAlchemy with the app
    db.init_app(app)

    # Connect Migrate with the app
    Migrate(app, db)

    from apps.crud import views as crud_views

    # Register the app using blueprint
    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    return app
