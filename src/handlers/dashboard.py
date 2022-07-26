from flask import Blueprint, render_template, request
from src.models.post import Post
from src.models.settings import db
from src.utils.user_helper import isLoggedIn, redirectToLogin, getCurrentUser
from src.utils.app_name import app_name

dashboard_handlers = Blueprint("dashboard", __name__)


@dashboard_handlers.route('/dashboard', methods=["GET"])
def dashboard():
    if request.method == "GET":
        if isLoggedIn():
            return render_template("dashboard.html",
                                   app_name=app_name,
                                   user=getCurrentUser(),
                                   posts=db.query(Post)
                                   .filter_by(deleted=False)
                                   .order_by(Post.created_at).all())
        else:
            return redirectToLogin()

    elif request.method == "GET":
        return render_template("404.html", app_name=app_name,
                               user=getCurrentUser())
