from wtforms.validators import DataRequired, Length, EqualTo, Email
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.fields.html5 import EmailField
from flask_wtf import FlaskForm


class QuestionForm(FlaskForm):

    subject = StringField("제목",   validators=[DataRequired("제목은 필수입력 항목입니다.")])
    content = TextAreaField("내용", validators=[DataRequired("내용은 필수입력 항목입니다.")])


class AnswerForm(FlaskForm):

    content = TextAreaField("내용", validators=[DataRequired("내용은 필수입력 항목입니다.")])


class UserCreateForm(FlaskForm):

    username  = StringField("사용자명",       validators=[DataRequired(), Length(min=4, max=25)])  # min=3
    password1 = PasswordField("비밀번호",     validators=[DataRequired(), EqualTo("password2", "비밀번호가 일치하지 않습니다.")])
    password2 = PasswordField("비밀번호 확인", validators=[DataRequired()])
    email     = EmailField("이메일",         validators=[DataRequired(), Email()])


class UserLoginForm(FlaskForm):

    username = StringField("사용자명",   validators=[DataRequired(), Length(min=4, max=25)])  # min=3
    password = PasswordField("비밀번호", validators=[DataRequired()])
