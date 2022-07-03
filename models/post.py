from models.settings import db
from datetime import datetime


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # database relationship  # noqa E501
    author = db.relationship("User")  # orm relationship
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=None)
    deleted_at = db.Column(db.DateTime, default=None)
    deleted = db.Column(db.Boolean, default=False)

    @classmethod
    def create(self, title, description, author):
        newPost = self(title=title, description=description,
                       author=author)
        db.add(newPost)
        db.commit()
        return newPost

    @classmethod
    def update(self, id, title, description):
        print(id)
        updatePost = db.query(Post).filter_by(id=id).first()
        print(updatePost)
        print(updatePost.title)
        print(updatePost.description)
        
        updatePost.title = title
        updatePost.description = description
        updatePost.updated_at = datetime.utcnow()

        db.add(updatePost)
        db.commit()
        return updatePost

    # def update(self, id, title, description, author,
    #            created_at, updated_at=datetime.utcnow()):
    #     updatePost = self(id=id, title=title, description=description,
    #                       author=author, created_at=created_at,
    #                       updated_at=updated_at)
    #     db.add(updatePost)
    #     db.commit()
    #     return updatePost

    @classmethod
    def delete(self, id, deleted, deleted_at=datetime.utcnow()):
        deletePost = self(id=id, deleted=deleted, deleted_at=deleted_at)
        db.add(deletePost)
        db.commit()
        return deletePost
