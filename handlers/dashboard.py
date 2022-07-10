from flask import render_template, Blueprint

from models.post import Post
from models.settings import db
from utils.user_helper import isLoggedIn, redirectToLogin, getCurrentUser

dashboard_handlers = Blueprint("dashboard", __name__)


@dashboard_handlers.route('/dashboard', methods=["GET"])  # http://localhost(/) M <-- V <-- View (HTML)  C <- Controller
def dashboard():
    if isLoggedIn():
        return render_template("dashboard.html", user=getCurrentUser(), posts=db.query(Post).all())
    else:
        return redirectToLogin()
