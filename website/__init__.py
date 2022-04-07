from email.mime import application
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"
#config database


def create_app():
    #membuat app
    app = Flask(__name__)
    #secret key untuk menencrypt cookies dan session
    app.config['SECRET_KEY'] = '487h312b3yu1g23yug12i3oi3hui1oh31y82g3'
    #config database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    #import blueprint 
    from .views import views
    from .auth import auth

    #register blueprint kedalam app
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Books,  Bookreturn,Bookborrow

    #memanggil method createdatabase
    create_database(app)

    #menghandle login 
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    #membuat database baru jika database tidak dideteksi
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
        





