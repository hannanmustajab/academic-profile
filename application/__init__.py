from flask import Flask, session
from flask_bcrypt import Bcrypt
from flask_session import Session
# from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '8924989289289289'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
bcrypt = Bcrypt(app)
# login_manager = LoginManager(app)

from application import routes
