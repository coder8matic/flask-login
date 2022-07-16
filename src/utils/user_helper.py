import json
from flask import make_response, redirect, request, url_for
# from src.models.settings import db
# from src.models.user import User
from src.utils.redis_settings import r


def isLoggedIn():
    session_token = request.cookies.get("session_token")
    user = getCurrentUser() if session_token else None

    return user is not None  # Returens True or False


def redirectToLogin():
    return redirectToRoute("auth.login")


def getCurrentUser():
    session_token = request.cookies.get("session_token")
    user_json = r.get(name=session_token)
    print(user_json)  # tmp
    if user_json is None:
        user = None
    else:
        user = json.loads(user_json)
        print(user)  # tmp
    return user


def redirectToRoute(route):
    return make_response(redirect(url_for(route)))
