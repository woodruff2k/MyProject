from myproject.config.default import *


SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(os.path.join(BASE_DIR, "myproject.db"))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "dev"