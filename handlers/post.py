from flask import render_template, request, Blueprint

from models.post import Post
from utils.user_helper import redirectToRoute, redirectToLogin, getCurrentUser, isLoggedIn

post_handlers = Blueprint("post", __name__)


@post_handlers.route('/post-add-form', methods=["GET"])
def post_form():
    return render_template("post_add_form.html") if isLoggedIn() else redirectToLogin()


@post_handlers.route('/post/<id>', methods=["GET", "DELETE", "POST"])
def handlePost():
    return "NOT IMPLEMENTED"


@post_handlers.route('/post', methods=["POST"])
def createPost():
    title = request.form.get('title')
    description = request.form.get('description')
    author = getCurrentUser()

    Post.create(title=title, description=description, author=author)

    return redirectToRoute("dashboard")
