from flask import Blueprint, url_for, redirect, request, render_template, session, g, flash
# from werkzeug.utils import redirect
from datetime import datetime
from .auth_views import login_required
from ..models import Question, Answer, User
from ..forms import AnswerForm
from .. import db


bp = Blueprint("answer", __name__, url_prefix="/answer")


@bp.before_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@bp.route("/create/<int:question_id>", methods=["POST"])
@login_required
def create(question_id):  # create_answer
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    if form.validate_on_submit():
        content = request.form["content"]
        # answer = Answer(content=content, created_at=datetime.now(), question=question)
        answer = Answer(content=content, created_at=datetime.now(), user=g.user)
        question.answer_set.append(answer)
        db.session.commit()
        return redirect(url_for("question.detail", question_id=question_id))
    # question_detail needs question object
    return render_template("question/question_detail.html", question=question, form=form)


@bp.route("/modify/<int:answer_id>", methods=["GET", "POST"])
@login_required
def modify(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if g.user != answer.user:
        flash("수정 권한이 없습니다.")
        return redirect(url_for("question.detail", question_id=answer.question.id))

    if request.method == "POST":
        form = AnswerForm()
        if form.validate_on_submit():
            # fill up the answer object
            form.populate_obj(answer)
            answer.modified_at = datetime.now()
            db.session.commit()
            return redirect(url_for('question.detail', question_id=answer.question.id))
    else:  # GET
        form = AnswerForm(obj=answer)
    # answer_form needs answer object
    return render_template("answer/answer_form.html", answer=answer, form=form)


@bp.route("/delete/<int:answer_id>")
@login_required
def delete(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if g.user != answer.user:
        flash("삭제 권한이 없습니다.")
    else:
        db.session.delete(answer)
        db.session.commit()
    question_id = answer.question.id
    return redirect(url_for('question.detail', question_id=question_id))
