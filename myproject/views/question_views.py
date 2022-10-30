from flask import Blueprint, render_template, request, redirect, url_for, session, g, flash, current_app
# from werkzeug.utils import redirect
from sqlalchemy import func, nullslast
from datetime import datetime
from .auth_views import login_required
from ..forms import QuestionForm, AnswerForm
from ..models import Question, User
from .. import db


bp = Blueprint("question", __name__, url_prefix="/question")


@bp.before_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


def _nullslast(obj):
    if current_app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite"):
        return obj
    else:
        return nullslast(obj)


@bp.route("/list/")
def list_():
    page_num = request.args.get("page", type=int, default=1)
    # question_list = Question.query.order_by(Question.created_at.desc())                 # BaseQuery obj
    # question_list = question_list.paginate(page_num, per_page=10).items                 # list obj
    # return render_template("question/question_list.html", question_list=question_list)  # list obj
    # question_query = Question.query.order_by(Question.created_at.desc())                # BaseQuery obj
    question_query = Question.query.order_by(Question.created_at.desc())                  # BaseQuery obj
    question_page = question_query.paginate(page_num, per_page=10)                        # Pagination obj
    return render_template("question/question_list.html", question_page=question_page)    # list obj


@bp.route("/detail/<int:question_id>/")
def detail(question_id):  # detail_question_with_answer
    form = AnswerForm()
    # question = Question.query.get(question_id)
    question = Question.query.get_or_404(question_id)
    # question_detail needs question object
    return render_template("question/question_detail.html", question=question, form=form)


@bp.route("/create/", methods=["GET", "POST"])
@login_required
def create():  # create_question
    form = QuestionForm()
    if request.method == "POST" and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data, created_at=datetime.now(), user=g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for("main.index"))
    return render_template("question/question_form.html", form=form)


@bp.route("/modify/<int:question_id>", methods=["GET", "POST"])
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash("수정 권한이 없습니다.")
        return redirect(url_for("question.detail", question_id=question_id))

    if request.method == "POST":
        form = QuestionForm()
        if form.validate_on_submit():
            # fill up the question object
            form.populate_obj(question)
            question.modified_at = datetime.now()
            db.session.commit()
            return redirect(url_for("question.detail", question_id=question_id))
    else:  # "GET"
        form = QuestionForm(obj=question)
    return render_template("question/question_form.html", form=form)


@bp.route("/delete/<int:question_id>")
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash("삭제 권한이 없습니다.")
        return redirect(url_for("question.detail", question_id=question_id))

    db.session.delete(question)
    db.session.commit()
    return redirect(url_for("question.list_"))
