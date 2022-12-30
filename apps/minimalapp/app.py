import json
import logging

from email_validator import EmailNotValidError, validate_email
from flask import (
    Flask,
    current_app,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

# Load flask secret key from another file and add it to app config
with open("secret.json", "r") as file:
    cred_data = json.load(file)
    flask_secret_key = cred_data["flask_secret_key"]

app.config["SECRET_KEY"] = flask_secret_key  # "2AZSMss3p5QPbcY2hBsJ"

# Set log level
app.logger.setLevel(logging.DEBUG)

# Do not intercept redirects
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

# Set the app in DebugToolbarExtension
toolbar = DebugToolbarExtension(app)


@app.route("/")
def index():
    return "Hello, Flaskbook!"


@app.route("/hello/<name>", methods=["GET"], endpoint="hello-endpoint")
def hello_name(name):
    return f"Hello, {name}!"


@app.route("/name/<name>")
def show_name(name):
    return render_template("index.html", name=name)


with app.test_request_context():
    print(url_for("index"))
    print(url_for("hello-endpoint", name="world"))
    print(url_for("show_name", name="ichiro", page="1"))
    print(url_for("static", filename="style.css"))


with app.test_request_context("/users?updated=true"):
    print(request.args.get("updated"))

# Contact Form
@app.route("/contact")
def contact():
    return render_template("contact.html")


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

        # Send an email here

        # Redirect to contact endpoint
        flash("Confirmation email was sent to your email address. Thank you!")
        return redirect(url_for("contact_complete"))

    return render_template("contact_complete.html")
