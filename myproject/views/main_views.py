from flask import Blueprint, url_for, redirect, session, g
# from werkzeug.utils import redirect
from flask_login import login_required
from ..views.auth_views import admin_login_required
from ..models import User


bp = Blueprint("main", __name__, url_prefix="/")


# @login_manager.user_loader
@bp.before_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@bp.route("/hello")
# @admin_login_required
@login_required
def hello_pybo():
    return "Hello, Pybo!"


@bp.route("/")
def index():
    # return "Pybo index"
    return redirect(url_for("question.list_"))