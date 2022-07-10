from flask import request, make_response, redirect, url_for;

from utils.redis import redis


def isLoggedIn():
    session_token = request.cookies.get("session_token")
    user = getCurrentUser() if session_token else None

    return user is not None


def redirectToLogin():
    return redirectToRoute("index")


def getCurrentUser():
    session_token = request.cookies.get("session_token")
    return redis.get(session_token)


def redirectToRoute(route):
    return make_response(redirect(url_for(route)))