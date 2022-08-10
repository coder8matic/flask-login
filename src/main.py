from flask import Flask, render_template
# load enviromental variables from .env file
from dotenv import load_dotenv
# Environment variables need to be imported before modules import
load_dotenv()

from src.handlers.auth import authentication_handlers  # noqa E402
from src.handlers.dashboard import dashboard_handlers  # noqa E402
from src.handlers.post import post_handlers  # noqa E402
from src.handlers.comment import comment_handlers  # noqa E402
from src.models.settings import db  # noqa E402
from src.models.comment import Comment  # noqa E402
from src.models.post import Post  # noqa E402
from src.models.user import User  # noqa E402
from src.utils.user_helper import isLoggedIn, redirectToRoute  # noqa E402
from src.utils.app_name import app_name  # noqa E402
from src.utils.user_helper import getCurrentUser  # noqa E402

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
app.register_blueprint(comment_handlers)


@app.route('/', methods=["GET"])
def index():
    return redirectToRoute("dashboard.dashboard") \
        if isLoggedIn() else redirectToRoute("auth.login")


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html", app_name=app_name,
                           user=getCurrentUser())


if __name__ == '__main__':
    app.run(use_reloader=True)
