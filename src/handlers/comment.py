from flask import Blueprint, render_template, request, redirect
from src.models.post import Post
from src.models.comment import Comment
from src.models.settings import db
from src.utils.app_name import app_name
from src.utils.user_helper import (getCurrentUser, isLoggedIn, redirectToLogin,
                                   redirectToRoute)

comment_handlers = Blueprint("comment_handlers", __name__)


@comment_handlers.route('/post_comments/<post_id>', methods=["GET", "POST"])
def postComments(post_id):
    getPost = db.query(Post).filter_by(id=post_id).first()
    if request.method == "GET":
        if getPost is None:
            return redirectToRoute("error.error404")   # redirect to 404
        getComments = db.query(Comment).filter_by(post_id=post_id) \
                                       .filter_by(deleted_at=None) \
                                       .order_by(Comment.created_at).all()
        print(getComments)
        return render_template("post_comments.html",
                               app_name=app_name,
                               post=getPost,
                               comments=getComments,
                               user=getCurrentUser()) \
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


@comment_handlers.route('/post_comments', methods=["POST"])
def updateComment():
    post_id = request.args.get('post_id', None)
    comment_id = request.args.get('comment_id', None)
    if request.method == "POST":
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
        # base_url = url_for(comment_handlers.PostComments(post_id))
        return redirect(f"/post_comments/{post_id}")  # TODO: change to variable path  # noqa E501


@comment_handlers.route('/delete_comments', methods=["POST"])
def deleteComment():
    post_id = request.args.get('post_id', None)
    comment_id = request.args.get('comment_id', None)
    if request.method == "POST":
        author_id = getCurrentUser().id
        deleteComment = db.query(Comment).filter_by(id=comment_id).first()
        if author_id == deleteComment.author_id:
            Comment.delete(id=comment_id)
            notification_msg = "You have deleted comment successfuly!"
            print(notification_msg)
        else:
            notification_msg = "You don't have permissions to delete comment!"
            print(notification_msg)
        # base_url = url_for(comment_handlers.PostComments(post_id))
        return redirect(f"/post_comments/{post_id}")  # TODO: change to variable path  
    # noqa E501