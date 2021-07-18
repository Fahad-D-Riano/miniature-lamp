from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'veryverylonglongsecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/todo_database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app


app = create_app()

import todo_app.models
import todo_app.login
import todo_app.admin
import todo_app.routes

