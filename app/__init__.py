from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,login_required,login_user,LoginManager,login_manager,current_user,logout_user

app = Flask(__name__,template_folder="../templates",static_folder='../static')
app.config['SECRET_KEY']='Thisisasecretkey'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app,session_options={"autoflush":False})
login_manager=LoginManager(app)

class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=-True)
    name=db.Column(db.String,nullable=False)
    email=db.Column(db.String(64),unique=True,index=True)
    password_hash=db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('Password is not readable attribute')
    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

class Files(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    file_name=db.Column(db.String,nullable=False,unique=True)
    file_path=db.Column(db.String,nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    file_type=db.Column(db.String,nullable=False)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))



from app import routes




