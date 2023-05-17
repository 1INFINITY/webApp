from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# init SQLAlchemy so we can use it later in our models

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website.db'
db = SQLAlchemy(app)

manager = LoginManager(app)
manager.login_view = 'auth.login'

# blueprint for auth routes in our app
from application.auth import auth as auth_blueprint

app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from application.main import main as main_blueprint

app.register_blueprint(main_blueprint)

app.app_context().push()
db.drop_all()
db.create_all()
app.run()