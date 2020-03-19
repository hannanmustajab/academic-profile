from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '8924989289289289'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from application import routes
