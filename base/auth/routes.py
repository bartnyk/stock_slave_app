from urllib.parse import urljoin, urlparse

from flask import Blueprint, flash, redirect, request, url_for
from flask_login import login_required, login_user

from base import cfg

from .auth import User

username_env = cfg.USERNAME
password_env = cfg.PASSWORD

blueprint = Blueprint("auth", __name__, url_prefix="/auth")


def is_safe_url(target):
    """Check if the redirect URL is safe."""
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == username_env and password == password_env:
            user = User(username=username)
            login_user(user)

            # Get the next page (if available) after login
            next_page = request.args.get("next")
            if next_page and is_safe_url(next_page):
                return redirect(next_page)
            return redirect(url_for("home"))
        else:
            flash("Invalid credentials")
            return redirect(url_for("login"))

    return """
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    """


@blueprint.route("/", methods=["GET", "POST"])
@login_required
def home():
    return "Hello, World!"
