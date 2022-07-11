from flask import Blueprint, render_template, request
from src.models.post import Post
from src.models.settings import db
from src.utils.app_name import app_name
from src.utils.user_helper import (getCurrentUser, isLoggedIn, redirectToLogin,
                                   redirectToRoute)

post_handlers = Blueprint("post_handlers", __name__)


@post_handlers.route('/post', methods=["GET", "POST"])
def createPost():
    if request.method == "GET":
        return render_template("post_new.html", app_name=app_name) \
            if isLoggedIn() else redirectToLogin()
    elif request.method == "POST":
        title = request.form.get('title')
        description = request.form.get('description')
        author = getCurrentUser()

        Post.create(title=title, description=description, author=author)

        return redirectToRoute("dashboard")


@post_handlers.route('/post/<post_id>', methods=["GET", "POST"])
def handlePost(post_id):
    if request.method == "GET":
        print("get method")
        handlePost = db.query(Post).filter_by(id=post_id).first()
        return render_template("post.html", app_name=app_name,
                               post_id=handlePost.id, title=handlePost.title,
                               description=handlePost.description) \
            if isLoggedIn() else redirectToLogin()

    elif request.method == "POST":
        if post_id is None:
            print("Post id is None")
            title = request.form.get('title')
            description = request.form.get('description')
            author = getCurrentUser()

            Post.create(title=title, description=description, author=author)

            return redirectToRoute("dashboard.dashboard")

        else:
            id = post_id
            title = request.form.get('title')
            description = request.form.get('description')
            Post.update(id=id, title=title, description=description)

            return redirectToRoute("dashboard.dashboard")


@post_handlers.route('/post/delete/<post_id>', methods=["POST"])
def deletePost(post_id):
    id = post_id
    Post.delete(id=id)

    return redirectToRoute("dashboard.dashboard")
