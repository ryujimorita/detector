from flask import Flask

def create_app():
    # Create a Flask instance
    app = Flask(__name__)

    from apps.crud import views as crud_views

    # Register the app using blueprint
    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    return app