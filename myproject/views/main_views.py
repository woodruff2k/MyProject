from flask import Blueprint, url_for, redirect, session, g, current_app
# from werkzeug.utils import redirect
from flask_login import login_required
# from ..views.auth_views import admin_login_required
from ..models import User


bp = Blueprint("main", __name__, url_prefix="/")


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
def hello():
    return "Hello, MyProject!"


@bp.route("/")
def index():
    # return "index"
    current_app.logger.info("INFO 레벨로 출력")
    return redirect(url_for("question.list_"))