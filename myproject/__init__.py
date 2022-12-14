from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from sqlalchemy import MetaData
from . import config


naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
# db = SQLAlchemy()
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()
login_manager = LoginManager()


def page_not_found(e):
    return render_template("404.html"), 404


def create_app():
    app = Flask(__name__)
    # app.config.from_object(config)
    # app.config.from_pyfile("/Users/sangwook.seo/Developments/pipeline/flaskbook/myproject/config/development.py")
    # app.config.from_pyfile("/Users/sangwook.seo/Developments/pipeline/flaskbook/myproject/config/production.py")
    # export APP_CONFIG_FILE=/Users/sangwook.seo/Developments/pipeline/flaskbook/myproject/config/development.py
    # export APP_CONFIG_FILE=/Users/sangwook.seo/Developments/pipeline/flaskbook/myproject/config/production.py
    app.config.from_envvar("APP_CONFIG_FILE")

    # ORM 초기화
    from . import models
    db.init_app(app)
    if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
    with app.app_context():
        db.create_all()
    login_manager.init_app(app)

    # Blueprint 초기화
    from .views import main_views, question_views, answer_views, auth_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)

    # Filter 초기화
    from .filter import format_datetime
    app.jinja_env.filters["datetime"] = format_datetime

    # Handler 초기화
    # 공통으로 적용할 HTTP 404과 500 에러 핸들러를 설정
    # 첫 번째 키는 blueprint, None는 어플리케이션 단위
    # app.error_handler_spec[None][404] = page_not_found
    app.register_error_handler(404, page_not_found)

    return app
