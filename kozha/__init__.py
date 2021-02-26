import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

# 서버가 처음 시작되었을 때 코드가 실행되는 부분 
app = Flask(__name__)
app.jinja_env.trim_blocks=True
app.config['SECRET_KEY']='627a18d6edde5c597e1be2a4a3307f00'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db' # sqlite database



db = SQLAlchemy(app)
migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
bcrypt = Bcrypt(app) #해쉬값 생성
login_manager = LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'anfuza@likelion.org'
app.config['MAIL_PASSWORD'] = '53837526'
mail = Mail(app)



from kozha import routes