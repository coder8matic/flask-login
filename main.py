from flask import Flask
import hashlib
from flask import render_template, request, make_response, redirect, url_for
from models.user import User
from models.post import Post
from models.settings import db
import uuid

app = Flask(__name__)
app_name = "myApp"


@app.route('/', methods=["GET"])
def index():
    return redirectToRoute("dashboard") if isLoggedIn() \
                                        else redirectToRoute("login")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", app_name=app_name)
    elif request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        tryUser = db.query(User).filter_by(email=email).first()

        if not tryUser:
            return "This user does not exist - try registration on /register"
        else:
            tryPassword = hashlib.sha256(password.encode()).hexdigest()
            if tryPassword == tryUser.password:
                tryUser.session_token = uuid.uuid4().__str__()
                db.add(tryUser)
                db.commit()

                response = make_response(redirect(url_for("dashboard")))
                response.set_cookie("session_token", tryUser.session_token,
                                    httponly=True, samesite='Strict')

                return response
            else:
                return "Wrong username/password!"


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        url = request.url_rule
        return render_template("register.html", app_name=app_name, url=url)
    elif request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        newUser = User(email=email, password=hashlib.sha256(password.encode())
                       .hexdigest())
        db.add(newUser)
        db.commit()
        return "You have been registered"


@app.route('/dashboard', methods=["GET"])
def dashboard():
    if isLoggedIn():
        return render_template("dashboard.html", app_name=app_name,
                               user=getCurrentUser(), posts=db.query(Post)
                               .all())
    else:
        return redirectToLogin()


@app.route('/post-form', methods=["GET"])
def post_form():
    return render_template("post_add_form.html", app_name=app_name) \
        if isLoggedIn() else redirectToLogin()


@app.route('/post/<post_id>', methods=["GET", "DELETE", "POST"])
def handlePost(post_id):
    if request.method == "GET":
        handlePost = db.query(Post).filter_by(id=post_id).first()
        return render_template("post.html", app_name=app_name,
                               post_id=handlePost.id, title=handlePost.title,
                               description=handlePost.description) \
            if isLoggedIn() else redirectToLogin()

    elif request.method == "POST":
        print(str(post_id) + "#100")
        if post_id is None:
            title = request.form.get('title')
            description = request.form.get('description')
            author = getCurrentUser()

            Post.create(title=title, description=description, author=author)

            return redirectToRoute("dashboard")

        else:
            id = post_id
            title = request.form.get('title')
            description = request.form.get('description')
            Post.update(id=id, title=title, description=description)

            return redirectToRoute("dashboard")

    elif request.method == "DELETE":
        return "NOT IMPLEMENTED"


@app.route('/post', methods=["POST"])
def createPost():
    title = request.form.get('title')
    description = request.form.get('description')
    author = getCurrentUser()

    Post.create(title=title, description=description, author=author)

    return redirectToRoute("dashboard")


def isLoggedIn():
    session_token = request.cookies.get("session_token")
    user = getCurrentUser() if session_token else None

    return user is not None


def redirectToLogin():
    return redirectToRoute("index")


def getCurrentUser():
    session_token = request.cookies.get("session_token")
    return db.query(User).filter_by(session_token=session_token).first()


def redirectToRoute(route):
    return make_response(redirect(url_for(route)))


if __name__ == '__main__':
    app.run(use_reloader=True, port=12345)
