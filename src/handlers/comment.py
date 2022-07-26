from flask import Blueprint, render_template, request, redirect, make_response, url_for
from src.models.post import Post
from src.models.comment import Comment
from src.models.settings import db
from src.utils.app_name import app_name
from src.utils.user_helper import (getCurrentUser, isLoggedIn, redirectToLogin,
                                   redirectToRoute)

comment_handlers = Blueprint("comment_handlers", __name__)


@comment_handlers.route('/post_comments/<post_id>', methods=["POST", "GET"])
def postComments(post_id):
    getPost = db.query(Post).filter_by(id=post_id).first()
    if request.method == "GET":
        if getPost is None:
            return render_template("404.html", app_name=app_name,
                           user=getCurrentUser())   # redirect to 404
        getComments = db.query(Comment).filter_by(post_id=post_id) \
                                       .filter_by(deleted_at=None) \
                                       .order_by(Comment.created_at).all()
        print(getComments)
        return render_template("post_comments.html",
                               app_name=app_name,
                               user=getCurrentUser(),
                               post=getPost,
                               comments=getComments) \
            if isLoggedIn() else redirectToLogin()
    elif request.method == "POST":
        comment = request.form.get('newComment')
        author_id = getCurrentUser().id

        Comment.create(post_id=post_id, comment=comment, author_id=author_id)
        getComments = db.query(Comment).filter_by(post_id=post_id) \
                                       .filter_by(deleted_at=None) \
                                       .order_by(Comment.created_at).all()
        return render_template("post_comments.html",
                               app_name=app_name,
                               post=getPost,
                               comments=getComments,
                               user=getCurrentUser()) \
            if isLoggedIn() else redirectToLogin()


@comment_handlers.route('/post_comments', methods=["POST", "GET"])
def updateComment():
    if request.method == "GET":
        return render_template("404.html", app_name=app_name,
                           user=getCurrentUser())

    elif request.method == "POST":
        post_id = request.args.get('post_id', None)
        comment_id = request.args.get('comment_id', None)
        author_id = getCurrentUser().id
        comment = request.form.get('updateComment')
        updateComment = db.query(Comment).filter_by(id=comment_id).first()
        if author_id == updateComment.author_id:
            Comment.update(id=comment_id, comment=comment, author_id=author_id)
            notification_msg = "You have deleted changed comment successfuly!"
            print(notification_msg)
        else:
            notification_msg = "You don't have permissions to change comment!"
            print(notification_msg)

    return make_response(redirect(url_for('comment_handlers.postComments', post_id=str(post_id))))


@comment_handlers.route('/delete_comments', methods=["POST", "GET"])
def deleteComment():
    if request.method == "GET":
        return render_template("404.html", app_name=app_name,
                           user=getCurrentUser())
    
    elif request.method == "POST":
        post_id = request.args.get('post_id', None)
        comment_id = request.args.get('comment_id', None)
        author_id = getCurrentUser().id
        deleteComment = db.query(Comment).filter_by(id=comment_id).first()
        if author_id == deleteComment.author_id:
            Comment.delete(id=comment_id)
            notification_msg = "You have deleted comment successfuly!"
            print(notification_msg)
        else:
            notification_msg = "You don't have permissions to delete comment!"
            print(notification_msg)

        return make_response(redirect(url_for('comment_handlers.postComments', post_id=str(post_id))))
