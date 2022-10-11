from flask import Flask
from flask_login import LoginManager
from functools import lru_cache
from flaskie_app import create_db

@lru_cache()
def create_app():
    db = create_db()
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    from models import Users
    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(id)

    return app