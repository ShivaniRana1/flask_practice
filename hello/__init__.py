from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)
app.config['SECRET_KEY'] = '37588adff654ba1e9fea38fbf58a1c8b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc:///?dsn=shivani.rana'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
title = " Details about the Farm"
db = SQLAlchemy(app)
login_manager = LoginManager(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'ranapriya123456789@gmail.com'
app.config['MAIL_PASSWORD'] = 'hhvlrjzfcagiaojc'
mail = Mail(app)
from hello import routes