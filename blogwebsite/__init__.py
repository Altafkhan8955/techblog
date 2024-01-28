from flask import Flask
from .database import db
from .model.model import UserModel
from flask_login import LoginManager
from flask_migrate import Migrate

UPLOAD_FOLDER = 'blogwebsite\static'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'altafkhantechblog'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/blog_db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = True
app.config['UPLOADS_To'] = 'uploads'


db.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return UserModel.query.get(int(id))

migrate = Migrate(app, db)

from blogwebsite import main