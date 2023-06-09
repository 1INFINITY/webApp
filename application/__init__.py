from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# init SQLAlchemy so we can use it later in our models

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website.db'
db = SQLAlchemy(app)

manager = LoginManager(app)
manager.login_view = 'auth.login'

from application.auth import auth as auth_blueprint

app.register_blueprint(auth_blueprint)

from application.main import main as main_blueprint

app.register_blueprint(main_blueprint)

from application.api import api as api_blueprint

app.register_blueprint(api_blueprint)

app.app_context().push()
db.create_all()
#db.drop_all()
app.run()