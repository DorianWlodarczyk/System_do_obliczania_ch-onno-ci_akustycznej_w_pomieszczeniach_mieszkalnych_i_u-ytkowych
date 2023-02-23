from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager

db = SQLAlchemy()
#DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    with app.app_context():
        app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
        #app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost:5432/app_akustyka'
        #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@db:5432/projekt'
        db.init_app(app)

        from .views import views
        from .auth import auth

        app.register_blueprint(views, url_prefix='/')
        app.register_blueprint(auth, url_prefix='/')

        from .models import Users, Notes

        #create_database(app)

        login_manager = LoginManager()
        login_manager.login_view = 'auth.login'
        login_manager.init_app(app)

        @login_manager.user_loader
        def load_user(id):
            return Users.query.get(int(id))

        return app


# def create_database(app):
#     if not path.exists('website/' + DB_NAME):
#         db.create_all()
#         print('Created Database!')
