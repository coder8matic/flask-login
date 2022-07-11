from flask import make_response, redirect, request, url_for
from src.models.settings import db
from src.models.user import User


def isLoggedIn():
    session_token = request.cookies.get("session_token")
    user = getCurrentUser() if session_token else None

    return user is not None


def redirectToLogin():
    return redirectToRoute("auth.login")


def getCurrentUser():
    session_token = request.cookies.get("session_token")
    return db.query(User).filter_by(session_token=session_token).first()


def redirectToRoute(route):
    return make_response(redirect(url_for(route)))
