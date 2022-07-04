from models.settings import db
from models.post import Post
from models.user import User

db.create_all()

# # Migrations to add delete button to post
# sql = db.text("ALTER TABLE posts ADD deleted_at DATETIME")
# db.execute(sql)

# sql = db.text("ALTER TABLE posts ADD deleted BOOLEAN")
# db.execute(sql)
