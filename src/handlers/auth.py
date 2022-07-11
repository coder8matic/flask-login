import hashlib
import uuid
from flask import (Blueprint, make_response, redirect, render_template,
                   request, url_for)
from src.main import app_name
from src.models.settings import db
from src.models.user import User

authentication_handlers = Blueprint("auth", __name__)


@authentication_handlers.route('/login', methods=["GET", "POST"])
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


@authentication_handlers.route('/register', methods=["GET", "POST"])
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
