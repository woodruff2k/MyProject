from flask_login import UserMixin
from myproject import db


class Question(db.Model):

    __tablename__ = "questions"

    id          = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    subject     = db.Column(db.String(200), nullable=False)
    content     = db.Column(db.Text,        nullable=False)
    created_at  = db.Column(db.DateTime,    nullable=False)
    modified_at = db.Column(db.DateTime,    nullable=True)
    # user_id   = db.Column(db.Integer,     db.ForeignKey("users.id", ondelete="CASCADE"), nullable=True, server_default="1")
    user_id     = db.Column(db.Integer,     db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user        = db.relationship("User",   backref=db.backref("question_set"))


class Answer(db.Model):

    __tablename__ = "answers"

    id          = db.Column(db.Integer,       primary_key=True, autoincrement=True)
    content     = db.Column(db.Text,          nullable=False)
    created_at  = db.Column(db.DateTime,      nullable=False)
    modified_at = db.Column(db.DateTime,      nullable=True)
    question_id = db.Column(db.Integer,       db.ForeignKey("questions.id", ondelete="CASCADE"))
    # source (Anwswer.question <-> Question.answer_set)
    # question  = db.relationship("Question", backref=db.backref("answer_set"))
    question    = db.relationship("Question", backref=db.backref("answer_set", cascade="all, delete-orphan"))
    # user_id   = db.Column(db.Integer,       db.ForeignKey("users.id", ondelete="CASCADE"), nullable=True, server_default="1")
    user_id     = db.Column(db.Integer,       db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user        = db.relationship("User",     backref=db.backref("answer_set"))

"""
class User(db.Model):

    __tablename__ = "users"

    id       = db.Column(db.Integer,    primary_key=True, autoincrement=True)
    username = db.Column(db.String(25),  unique=True, nullable=False)  # db.String(150)
    email    = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(25),  nullable=False)               # db.String(200)
"""


class User(db.Model, UserMixin):

    __tablename__ = "users"

    id         = db.Column(db.Integer,    primary_key=True, autoincrement=True)
    username   = db.Column(db.String(25), unique=True)  # db.String(100)
    email      = db.Column(db.String(50), unique=True)
    password   = db.Column(db.String(120))              # db.String(255)
    created_at = db.Column(db.DateTime)

    rank       = db.Column(db.Integer, default=1)
    point      = db.Column(db.Integer, default=0)

    @property
    def is_admin(self):
        user = User.query.filter(User.id == self.get_id()).first()
        if not (user and user.rank):
            return False
        if user.rank < 2:
            return False
        # user.rank >= 2
        return True
