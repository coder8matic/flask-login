import hashlib
import json
import uuid

from flask import render_template, request, make_response, redirect, url_for, Blueprint

from models.settings import db
from models.user import User
from utils.redis import redis

authentication_handlers = Blueprint("auth", __name__)


@authentication_handlers.route('/', methods=["GET"])  # http://localhost(/) M <-- V <-- View (HTML)  C <- COntroller
def index():
    return render_template("index.html")


@authentication_handlers.route('/login', methods=["POST"])  # http://localhost(/) M <-- V <-- View (HTML)  C <- COntroller
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    tryUser = db.query(User).filter_by(email=email).first()

    if not tryUser:
        return "This user does not exist - try registration on /register"
    else:
        tryPassword = hashlib.sha256(password.encode()).hexdigest()
        # print(tryUser)
        # exit()
        if tryPassword == tryUser.password:
            # tryUser.session_token = uuid.uuid4()
            # db.commit(tryUser) { session_token : "token" }
            # db.query(User).filter_by(email=email).update(dict(session_token=uuid.uuid4().__str__()))
            # db.commit()
            # tryUser.session_token = uuid.uuid4().__str__()
            # db.add(tryUser)
            # db.commit()

            session_token = uuid.uuid4().__str__()

            # {
            #   'hjkkuyhjkuy65789' : {'email': 'nekemail', 'password',.....}
            # }
            redis.set(name=session_token, value=json.dumps({
                'email': tryUser.email,
                'password': tryUser.password,
            }))

            response = make_response(redirect(url_for("dashboard")))
            # print(response)
            # exit()
            response.set_cookie("session_token", session_token, httponly=True, samesite='Strict')

            return response
        else:
            return "Wrong username/password!"


@authentication_handlers.route('/register', methods=["GET", "POST"])  # http://localhost(/) M <-- V <-- View (HTML)  C <- Controller
def register():
    if request.method == "GET":
        url = request.url_rule
        return render_template("register.html", url=url)
    elif request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        newUser = User(email=email, password=hashlib.sha256(password.encode()).hexdigest())
        db.add(newUser)
        db.commit()
        return "Sučes"
