from flask import Blueprint, url_for, render_template, flash, request, redirect, session, g
# from werkzeug.utils import redirect
from flask_login import current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from ..forms import UserCreateForm, UserLoginForm
from ..models import User
from .. import db, login_manager


# bp = Blueprint("auth", __name__, url_prefix="/auth")
bp = Blueprint("users", __name__, url_prefix="/users")


@bp.before_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


# for flask_login (current_user)
@login_manager.user_loader
def load_user(user_id):  # user.id
    return User.query.get(user_id)


def login_required(view):

    @wraps(view)
    def wrapped_view(*args, **kwargs):

        # def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("users.login"))
        # return view(**kwargs)
        return view(*args, **kwargs)

    return wrapped_view


# for flask_login (current_user)
def admin_login_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect("/users/login?auth")

        if not current_user.is_admin:
            return redirect("/users/login?admin")

        return f(*args, **kwargs)

    return decorated


# @bp.route("/signup/", methods=["GET", "POST"])
@bp.route("/regist", methods=["GET", "POST"])
def regist():  # signup():
    form = UserCreateForm()
    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            # error = "존재하지 않는 사용자입니다."
            user = User(username=form.username.data, password=generate_password_hash(form.password1.data),
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("main.index"))
        else:
            flash("이미 존재하는 사용자입니다.")
    return render_template("auth/signup.html", form=form)


# @bp.route("/login/", methods=["GET", "POST"])
@bp.route("/login", methods=["GET", "POST"])
def login():
    form = UserLoginForm()
    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        error = None
        if user is None:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session["user_id"] = user.id
            # for flask_login (current_user)
            login_user(user)
            return redirect(url_for("main.index"))
        flash(error)
    return render_template("auth/login.html", form=form)


@bp.route("/logout")
def logout():
    session.clear()
    # for flask_login (current_user)
    logout_user()
    return redirect(url_for("main.index"))
