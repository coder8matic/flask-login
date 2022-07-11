from flask import Blueprint, render_template
from src.models.post import Post
from src.models.settings import db
from src.utils.user_helper import isLoggedIn, redirectToLogin, getCurrentUser
from src.main import app_name

dashboard_handlers = Blueprint("dashboard", __name__)


@dashboard_handlers.route('/dashboard', methods=["GET"])
def dashboard():
    if isLoggedIn():
        return render_template("dashboard.html", app_name=app_name,
                               user=getCurrentUser(), posts=db.query(Post)
                               .filter_by(deleted=False).all())
    else:
        return redirectToLogin()
