from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from forecastapp.config import Config
import logging

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    logging.basicConfig(filename='wickedtools.log',level=logging.INFO)

    # the imports below refer to the variables created in routes.py files that
    # initialize the named blueprints (package)
    from forecastapp.users.routes import users
    from forecastapp.posts.routes import posts
    from forecastapp.main.routes import main
    from forecastapp.reportgen.routes import reportgen
    from forecastapp.db_mgmt.routes import db_mgmt
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(reportgen)
    app.register_blueprint(db_mgmt)

    return app
