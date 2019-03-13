from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR SECRET KEY GOES HERE - needed for sessions'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c1843449:1337Parrot_98@csmysql.cs.cf.ac.uk:3306/c1843449'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

from shop import routes
