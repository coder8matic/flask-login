import json
from flask import make_response, redirect, request, url_for
# from src.models.settings import db
from src.models.user import User
from src.utils.redis_settings import r


def isLoggedIn():
    session_token = request.cookies.get("session_token")
    logged_user = getCurrentUser() if session_token else None

    return logged_user is not None  # Returens True or False


def redirectToLogin():
    return redirectToRoute("auth.login")


def getCurrentUser():
    session_token = request.cookies.get("session_token")
    user_redis = r.get(name=session_token)
    if user_redis is None:
        User is None
    else:
        user_json = json.loads(user_redis)
        User.id = user_json.get('id')
        User.email = user_json.get('email')
        User.password = user_json.get('password')

    return User


def redirectToRoute(route):
    return make_response(redirect(url_for(route)))
