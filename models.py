from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import sqlite3

from flask_login import LoginManager, UserMixin


from werkzeug.security import check_password_hash 
login_manager = LoginManager()
db = SQLAlchemy()

# Inherit all necessary methods from UserMixin class
class User(UserMixin,db.Model) :
    """Create columuns to store our data"""
    # id, username, email, password
    # User.query.all()===@
    # User.query.filter_by(usename="James").first()
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    
    def __init__(self, username, email, password) :
        self.username = username
        self.email = email
        self.password = password
        
    def __repr__(self) :
        #return '<User %r>' % self.username
        return f"({self.username} {self.email})"
    
    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)


class Course(db.Model) :
    """Create this course table to store course details"""
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    instructor = db.Column(db.String(80), nullable=False)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)
    


