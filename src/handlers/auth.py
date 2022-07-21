import hashlib
import json
import uuid

from flask import (Blueprint, make_response, redirect, render_template,
                   request, url_for)
from src.models.settings import db
from src.models.user import User
from src.utils.app_name import app_name
from src.utils.redis_settings import r

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
                session_token = uuid.uuid4().__str__()
                # insert into redis
                r.set(name=session_token, value=json.dumps({
                   'id': tryUser.id,
                   'email': tryUser.email,
                   'password': tryUser.password
                }))

                response = make_response(redirect(url_for("dashboard.dashboard")))  # noqa E501
                response.set_cookie("session_token", session_token,
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


@authentication_handlers.route('/logout', methods=["POST"])
def logout():
    if request.method == "POST":
        session_token = request.cookies.get("session_token")
        r.delete(name=session_token)
        request.cookies.clear("session_token")
    
    response = make_response(redirect(url_for("dashboard.dashboard")))
    return response
