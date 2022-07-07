from models.settings import db


class Abstract(db.Model):

    @classmethod
    def filter_by(cls, **kwargs):
        return db.Model.filter_by(kwargs, deleted_at = None)

    @classmethod
    def filter_by_with_deleted(cls, **kwargs):
        return db.Model.filter_by(kwargs)
