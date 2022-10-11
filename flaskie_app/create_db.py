from flask_sqlalchemy import SQLAlchemy
from functools import lru_cache

@lru_cache()
def create_db():
    db = SQLAlchemy()
    return db