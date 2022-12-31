import json
import logging
import os

from email_validator import EmailNotValidError, validate_email
from flask import (
    Flask,
    current_app,
    flash,
    g,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail, Message

# Create a Flask instance
app = Flask(__name__)


# Load flask secret key from another file and add it to app config
with open("secret.json", "r") as file:
    cred_data = json.load(file)
    flask_secret_key = cred_data["flask_secret_key"]
    gmail_username = cred_data["gmail_username"]
    gmail_app_password = cred_data["gmail_app_password"]

app.config["SECRET_KEY"] = flask_secret_key

# Set log level
app.logger.setLevel(logging.DEBUG)

# Do not intercept redirects
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

# Set the app in DebugToolbarExtension
toolbar = DebugToolbarExtension(app)

# Email
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")


def send_email(recipient: str, subject: str, template: str, **kwargs) -> None:
    """Send an email after submit the contact form."""
    msg = Message(subject, recipients=[recipient])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)


# Wrap app with flask-mail
mail = Mail(app)


@app.route("/")
def index():
    return "Hello!"


@app.route("/hello/<name>", methods=["GET"], endpoint="hello-endpoint")
def hello_name(name):
    return f"Hello, {name}!"


@app.route("/name/<name>")
def show_name(name):
    return render_template("index.html", name=name)


# Contact Form
@app.route("/contact")
def contact():
    # Get response object
    response = make_response(render_template("contact.html"))

    # Set cookie
    response.set_cookie("flask key", "flask value")

    # Session
    session["username"] = "John Doe"

    return response


# Contact Complete
@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":
        # Get values from contact form submission
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]

        # Validate input
        is_valid = True

        if not username:
            flash("User name is required")
            is_valid = False

        if not email:
            flash("Email address is required")
            is_valid = False

        try:
            validate_email(email)
        except EmailNotValidError:
            flash("Please a correct email address")
            is_valid = False

        if not description:
            flash("Inquiry details cannot be empty")
            is_valid = False

        if not is_valid:
            return redirect(url_for("contact"))

        # Send an email
        send_email(
            recipient=email,
            subject="Thank you for your inquiry!",
            template="contact_mail",
            username=username,
            description=description,
        )

        # Redirect to contact endpoint
        flash("Confirmation email was sent to your email address. Thank you!")
        return redirect(url_for("contact_complete"))

    return render_template("contact_complete.html")
