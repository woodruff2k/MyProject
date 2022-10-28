from logging.config import dictConfig
from myproject.config.default import *


# SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(os.path.join(BASE_DIR, "myproject.db"))
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{user}:{pw}@{url}/{db}".format(
    user="dbmasteruser",
    pw="Sswlovescjy7*",
    url="ls-667112f99a05e19881247d528e8a4cd898ae344c.cirydvrpoxy7.ap-northeast-2.rds.amazonaws.com",
    db="myproject"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "prod"

dictConfig({
    "version": 1,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
        }
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "logs/myproject.log"),
            "maxBytes": 1024*1024*5,  # 5 MB
            "backupCount": 5,
            "formatter": "default",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["file"]
    }
})
