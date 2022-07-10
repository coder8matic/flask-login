from flask import Blueprint, render_template
from models.post import Post
from models.settings import db
from utils.user_helper import isLoggedIn, redirectToLogin, getCurrentUser
from main import app_name

dashboard_handlers = Blueprint("dashboard", __name__)


@dashboard_handlers.route('/dashboard', methods=["GET"])
def dashboard():
    if isLoggedIn():
        return render_template("dashboard.html", app_name=app_name,
                               user=getCurrentUser(), posts=db.query(Post)
                               .filter_by(deleted=False).all())
    else:
        return redirectToLogin()
