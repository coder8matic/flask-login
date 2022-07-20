from flask import Blueprint, render_template
from src.utils.user_helper import getCurrentUser
from src.utils.app_name import app_name

error_handlers = Blueprint("error", __name__)


@error_handlers.route('/404', methods=["GET"])
def error404():
    return render_template("404.html", app_name=app_name,
                           user=getCurrentUser())
