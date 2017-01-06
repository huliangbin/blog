from flask import Flask
from flask.ext.wtf import CsrfProtect
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
# csrf = CsrfProtect()
# csrf.init_app(app)

# flask_login
lm = LoginManager()
lm.init_app(app)

# mysql
db = SQLAlchemy(app)

from src.models import user, post, comment
from src.views import index, login, edit
