from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_database(app):
    basedir = os.path.abspath(os.path.join(app.root_path, '..'))
    with app.app_context():
        path = os.path.join(basedir, 'db')
        if not os.path.exists(path):
            os.makedirs(path)
        db.create_all()
    print("Database tables created (if they didn't exist already).")
