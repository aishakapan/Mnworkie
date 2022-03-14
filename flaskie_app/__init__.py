from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager



db = SQLAlchemy()

def create_app():


    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    from .models import Users
    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(id)

    return app

app = create_app()
import flaskie_app.views