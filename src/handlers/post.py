from flask import Blueprint, render_template, request
from src.models.post import Post
from src.models.settings import db
from src.utils.app_name import app_name
from src.utils.user_helper import (getCurrentUser, isLoggedIn, redirectToLogin,
                                   redirectToRoute)

post_handlers = Blueprint("post_handlers", __name__)


@post_handlers.route('/new_post', methods=["GET", "POST"])
def createPost():
    if request.method == "GET":
        return render_template("post_new.html", app_name=app_name, user=getCurrentUser()) \
            if isLoggedIn() else redirectToLogin()
    elif request.method == "POST":
        title = request.form.get('title')
        description = request.form.get('description')
        author = getCurrentUser()

        Post.create(title=title, description=description, author_id=author.id)

        return redirectToRoute("dashboard.dashboard")


@post_handlers.route('/post/<post_id>', methods=["GET", "POST"])
def handlePost(post_id):
    if request.method == "GET":
        print("get method")
        handlePost = db.query(Post).filter_by(id=post_id).first()
        if handlePost is None:
            return redirectToRoute("error.error404")   # redirect to 404
        else:
            return render_template("post_edit.html", app_name=app_name, user=getCurrentUser(),
                                   id=handlePost.id, title=handlePost.title,
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
            author = getCurrentUser()
            post = db.query(Post).filter_by(id=id).first()
            if author.id == post.author_id:
                Post.update(id=id, title=title, description=description)
                notification_msg = "You have changed post successfully!"
                print(notification_msg)
            else:
                notification_msg = "You don't have permissions to change post!"
                print(notification_msg)
            return redirectToRoute("dashboard.dashboard")


@post_handlers.route('/post/delete/<post_id>', methods=["POST", "GET"])
def deletePost(post_id):
    if request.method == "GET":
        return render_template("404.html", app_name=app_name, user=getCurrentUser(),
                           user=getCurrentUser())

    elif request.method == "POST":
        id = post_id
        author = getCurrentUser()
        post = db.query(Post).filter_by(id=id).first()
        if author.id == post.author_id:
            Post.delete(id=id)
            notification_msg = "You have deleted post successfully!"
            print(notification_msg)
        else:
            notification_msg = "You don't have permissions to delete post!"
            print(notification_msg)

        return redirectToRoute("dashboard.dashboard")
