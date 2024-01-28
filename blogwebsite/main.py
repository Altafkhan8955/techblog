from blogwebsite import app
from flask import flash, redirect,render_template,url_for,request,session
from blogwebsite.database import db
from .model.model import UserModel,ContactModel,CategoryMaster,BlogModel,BlogComment,SubComment
from flask_login import current_user, login_user, logout_user
from .middleware import auth, guest
from datetime import datetime
from sqlalchemy import or_
import base64
import os
from io import BytesIO

def get_all_categories():
    try:
        global global_all_category_no, global_all_category_name
        all_category_info = db.session.query(CategoryMaster.category_id,CategoryMaster.category_name)
        all_category_info = list(all_category_info)
        global_all_category_no, global_all_category_name = zip(*all_category_info)
    except Exception as e:
        pass   
    
@app.before_request
def create_all():
    #db.create_all()
    get_all_categories()

@app.route('/')
def home():
    try:
        all_self_blogs = BlogModel.query.all()
        return render_template('index.html',all_self_blogs = all_self_blogs, all_categories = global_all_category_name)
    except Exception as e:
        return render_template('index.html')

@app.route('/register',methods=['POST','GET'])
@guest
def register():
    if request.method == "POST":
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        
        if UserModel.query.filter_by(email=email).first():
            flash("Email already exist!", 'danger')
            return render_template('authentication/register.html')
        if UserModel.query.filter_by(username=username).first():
            flash("Username already exists!", 'danger')
            return render_template('authentication/register.html')
        if len(password) < 6:
            flash("Password length long by 6!", 'warning')
            return render_template('authentication/register.html')
        user = UserModel(email=email,username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("User register successful!", 'success')
        return redirect(url_for('login'))
    return render_template('authentication/register.html')

@app.route('/login', methods=['GET','POST'])
@guest
def login():
    if request.method == "POST":
        email = request.form.get('email')
        user = UserModel.query.filter_by(email=email).first()
        if user is not None and user.check_password(request.form.get('password')):
            session['email']=user.email
            login_user(user)
            return redirect('/')
        else:
            flash("Email and password doesn't match!", 'danger')
            return redirect(url_for('login'))
    return render_template('authentication/login.html')

@app.route('/logout')
def logout():
    logout_user()
    flash("User logout successful!", 'success')
    return redirect('/login')

@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == "POST":
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        message = request.form.get('message')
        contact = ContactModel(fullname=fullname,email=email,message=message)
        db.session.add(contact)
        db.session.commit()
        flash("Your response add successful!", 'success')
        return redirect(url_for('contact'))
    return render_template('authentication/contact.html')

@app.route('/blog_detail/<int:blog_model_id>/<string:blog_model_category>',methods=['GET','POST'])
def blog_detail(blog_model_id, blog_model_category):
    blog_model = BlogModel.query.get(blog_model_id)
    comment = BlogComment.query.filter_by(blog_id=blog_model_id)
    sub_comment = SubComment.query.filter(or_(
            SubComment.blogcomment_id ==1 ,))
    blog_model.blog_read_count = blog_model.blog_read_count + 1
    db.session.commit()
    return render_template('blog_details.html',blog_id=blog_model_id, blog_categories = blog_model_category,blog_model = blog_model,comment=comment,sub_comment=sub_comment)


@app.route('/blog_comment', methods=['GET','POST'])
def blog_comment():
    try:
        if request.method == 'POST':
            blog_id = request.form.get('blog_id')
            name = request.form.get('name')
            email = request.form.get('email')
            blog_comment = request.form.get('message')
            today = datetime.now()
            newComment = BlogComment(
                blog_id = blog_id,
                name = name,
                email = email,
                blog_comment = blog_comment,
                blog_comment_date = today            
            )
            db.session.add(newComment)
            db.session.commit()
            flash('Comment add successful!', 'success')
            return redirect(url_for('home'))
    except Exception as e:
        flash('Comment not add please try again!', 'danger')
        return redirect(url_for('home'))
    
@app.route('/sub_comment', methods=['GET','POST'])
def sub_comment():
    try:
        if request.method == 'POST':
            #blog_id = request.form.get('blog_id')
            blog_id = request.form.get('blog_id')
            name = request.form.get('name')
            email = request.form.get('email')
            blog_comment = request.form.get('message')
            today = datetime.now()
            new_subcomment = SubComment(
                #blogcomment_id = blogcomment_id,
                blog_id=blog_id,
                name = name,
                email = email,
                blog_comment = blog_comment,
                blog_comment_date = today            
            )
            print("data subcomment",new_subcomment)
            db.session.add(new_subcomment)
            db.session.commit()
            flash('Comment add successful!', 'success')
            return redirect(url_for('home'))
    except Exception as e:
        flash('Comment not add please try again!', 'danger')
        return redirect(url_for('home'))
    
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        squery = request.args.get('search_query')
        try:
            all_self_blogs = BlogModel.query.filter(or_(
                BlogModel.writer_name == squery,
                BlogModel.blog_title == squery,)).all()
            return render_template('search.html',all_self_blogs = all_self_blogs, all_categories = global_all_category_name)
        except Exception as e:
            return render_template('not_found.html')
 
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')

@app.errorhandler(500)
def not_found(e):
    return render_template('500.html')        