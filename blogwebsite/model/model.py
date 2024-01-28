from blogwebsite.database import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

class UserModel(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    contact_number = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    def is_active(self):
        return True
    
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    
class CategoryMaster(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(120), nullable = False)
    blogmodel = db.relationship('BlogModel', backref='categorymaster',lazy=True)

class BlogModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    category_id = db.Column(db.Integer,db.ForeignKey('category_master.category_id'), nullable=False)
    writer_name = db.Column(db.String(50), nullable=False)
    blog_title = db.Column(db.String(120), nullable=False)
    blog_text = db.Column(db.Text, nullable=False)
    blog_creation_date = db.Column(db.DateTime)
    image = db.Column(db.String(255))
    image_data = db.Column(db.String(255))
    blog_read_count = db.Column(db.Integer, default=0)

class BlogComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blog_id = db.Column(db.Integer,db.ForeignKey('blog_model.id'), nullable=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    blog_comment = db.Column(db.Text)
    blog_comment_date = db.Column(db.DateTime)
    
class SubComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blogcomment_id = db.Column(db.Integer,db.ForeignKey('blog_comment.id'))
    blog_id = db.Column(db.Integer,db.ForeignKey('blog_model.id'))
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    blog_comment = db.Column(db.Text)
    blog_comment_date = db.Column(db.DateTime)
    
class ContactModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(120), nullable = False)
    email = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text)
    
