from flask import Blueprint, render_template, request
from src.models.post import Post
from src.models.comment import Comment
from src.models.settings import db
from src.utils.app_name import app_name
from src.utils.user_helper import (getCurrentUser, isLoggedIn, redirectToLogin,
                                   redirectToRoute)

post_handlers = Blueprint("post_handlers", __name__)


@post_handlers.route('/comment/<post_id>', methods=["GET", "POST"])
def CommentPost(post_id):
    if request.method == "GET":
        getPost = db.query(Post).filter_by(id=post_id).first()
        if getPost is None:
            return redirectToRoute("error.error404")   # redirect to 404
        getComments = db.query(Comment).filter_by(post_id=post_id).all()
        return render_template("post_comments.html",
                               app_name=app_name,
                               post=getPost,
                               comments=getComments,
                               user=getCurrentUser()) \
            if isLoggedIn() else redirectToLogin()
    # elif request.method == "POST":
    #     title = request.form.get('title')
    #     description = request.form.get('description')
    #     author = getCurrentUser()

    #     Post.create(title=title, description=description, author=author)

    #    return redirectToRoute("dashboard.dashboard")


# @post_handlers.route('/post/<post_id>', methods=["GET", "POST"])
# def handlePost(post_id):
#     if request.method == "GET":
#         print("get method")
#         handlePost = db.query(Post).filter_by(id=post_id).first()
#         if handlePost is None:
#             return redirectToRoute("error.error404")   # redirect to 404
#         else:
#             return render_template("post_edit.html", app_name=app_name,
#                                    id=handlePost.id, title=handlePost.title,
#                                    description=handlePost.description) \
#                 if isLoggedIn() else redirectToLogin()

#     elif request.method == "POST":
#         if post_id is None:
#             print("Post id is None")
#             title = request.form.get('title')
#             description = request.form.get('description')
#             author = getCurrentUser()

#             Post.create(title=title, description=description, author=author)

#             return redirectToRoute("dashboard.dashboard")

#         else:
#             id = post_id
#             title = request.form.get('title')
#             description = request.form.get('description')
#             Post.update(id=id, title=title, description=description)

#             return redirectToRoute("dashboard.dashboard")


# @post_handlers.route('/post/delete/<post_id>', methods=["POST"])
# def deletePost(post_id):
#     id = post_id
#     Post.delete(id=id)

#     return redirectToRoute("dashboard.dashboard")
