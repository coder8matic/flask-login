from flask import Flask
from src.handlers.auth import authentication_handlers
from src.handlers.dashboard import dashboard_handlers
from src.handlers.post import post_handlers
from src.handlers.error import error_handlers
from src.models.settings import db
from src.models.comment import Comment
from src.models.post import Post
from src.models.user import User
from src.utils.user_helper import isLoggedIn, redirectToRoute

# Check if everything is OK with DB. If DB do not exist create DB
try:
    db.query(User).first()
    print("Table Users is OK")
    db.query(Post).first()
    print("Table Posts is OK")
    db.query(Comment).first()
    print("Table Comments is OK")
except:   # noqa E722
    try:
        db.create_all()
        print("DB created")
    except:   # noqa E722
        print("Something went wrong with DB check procedure")
# end of DB check


app = Flask(__name__)
app.register_blueprint(authentication_handlers)
app.register_blueprint(dashboard_handlers)
app.register_blueprint(post_handlers)
app.register_blueprint(error_handlers)


@app.route('/', methods=["GET"])
def index():
    return redirectToRoute("dashboard.dashboard") if isLoggedIn() \
                                        else redirectToRoute("auth.login")


if __name__ == '__main__':
    app.run(use_reloader=True)
