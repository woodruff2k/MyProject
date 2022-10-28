from logging.config import dictConfig
from myproject.config.default import *


SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(os.path.join(BASE_DIR, "myproject.db"))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "dev"

dictConfig({
    "version": 1,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
        }
    },
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "logs/myproject.log"),
            "maxBytes": 1024*1024*5,  # 5 MB
            "backupCount": 5,
            "formatter": "default",
        },
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["file"]
    }
})
