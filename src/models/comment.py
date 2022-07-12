from datetime import datetime
from src.models.settings import db


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.String)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # database relationship  # noqa E501
    author = db.relationship("User")  # orm relationship

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))  # database relationship  # noqa E501
    post = db.relationship("Post")  # orm relationship

    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=None)
    deleted_at = db.Column(db.DateTime, default=None)
    deleted = db.Column(db.Boolean, default=False)

    @classmethod
    def create(self, post_id, comment, author):
        newComment = self(post_id=post_id, comment=comment,
                          author=author)
        db.add(newComment)
        db.commit()
        return newComment

    @classmethod
    def update(self, id, post_id, comment):
        updateComment = db.query(Comment).filter_by(id=id).first()
        updateComment.post_id = post_id
        updateComment.comment = comment
        updateComment.updated_at = datetime.utcnow()

        db.add(updateComment)
        db.commit()
        return updateComment

    @classmethod
    def delete(self, id):
        deleteComment = db.query(Comment).filter_by(id=id).first()
        deleteComment.deleted = True
        deleteComment.deleted_at = datetime.utcnow()

        db.add(deleteComment)
        db.commit()
        return deleteComment
