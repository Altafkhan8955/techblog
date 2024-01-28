from siteadmin import siteadmin
from blogwebsite import app,UPLOAD_FOLDER
from flask import flash, render_template,redirect,url_for,request,session
from flask_login import logout_user
from blogwebsite.middleware import admin_auth
from blogwebsite.database import db
from blogwebsite.model.model import CategoryMaster,BlogModel,BlogComment,SubComment,ContactModel
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
        


    
@siteadmin.before_app_request
def create_all():
   # db.create_all()
    get_all_categories()



@siteadmin.route('/dashboard', methods=['GET', 'POST'])
@admin_auth
def dashboard():
    blog = BlogModel.query.all()
    return render_template('home.html',blog=blog)

@siteadmin.route('/admin_login', methods=['GET','POST'])
def admin_login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'admin' and password == 'admin':
            session['username'] = username
            return redirect(url_for('siteadmin.dashboard'))
        else:
            flash("Username and password doesn't match!", 'danger')
            return redirect('admin_login')
    return render_template('admin_login.html')

@siteadmin.route('/admin_logout')
@admin_auth
def admin_logout():
    session.pop('username',None)
    logout_user()
    flash("User logout successful!", 'success')
    return redirect('admin_login')

###################insert Blogmodel admin###############################
@siteadmin.route('/insert_blog', methods=['GET', 'POST'])
@admin_auth
def insert_blog():
    try:
        if request.method == "POST":
            category_id = request.form.get('category_id')
            writer_name = request.form.get('writer_name')
            blog_title = request.form.get('blog_title')
            blog_text = request.form.get('blog_text')
            file = request.files['file']
            today = datetime.now()
            blog_read_count = 0
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            newBlog = BlogModel(category_id=category_id,
                   writer_name=writer_name,
                   blog_title=blog_title,
                   blog_text = blog_text,
                   blog_creation_date = today,
                   image = filename,
                   blog_read_count = blog_read_count,
                    )
            db.session.add(newBlog)
            db.session.commit()
            flash('Blog insert successfull', 'success')
            return redirect(url_for('siteadmin.insert_blog'))
    except Exception as e:
        flash('Blog not insert please try again!','info')
        return redirect(url_for('siteadmin.insert_blog'))
    return render_template('insert_blog.html',all_category_id = global_all_category_no,all_category_name = global_all_category_name)

@siteadmin.route('/blog_filte', methods=['GET','POST'])
@admin_auth
def blog_filte():
    try:
        if request.method == 'GET':
            bquery = request.args.get('bquery')
            blog = BlogModel.query.filter(or_(
            BlogModel.writer_name == bquery,
            BlogModel.blog_title == bquery,
            BlogModel.blog_creation_date == bquery,
            BlogModel.blog_read_count == bquery,)).all()
            return render_template('home.html',blog=blog)
    except Exception as e:
        flash('Request filter not perform!', 'warning')
        return redirect(url_for('siteadmin.dashboard'))
    
@siteadmin.route('/update_blog/<int:id>', methods=['GET','POST'])
@admin_auth
def update_blog(id):
    blog = BlogModel.query.get(id)
    try:
        if request.method == "POST":
            blog.category_id = request.form.get('category_id')
            blog.writer_name = request.form.get('writer_name')
            blog.blog_title = request.form.get('blog_title')
            blog.blog_text = request.form.get('blog_text')
            db.session.commit()
            flash('Blog Update successful!', 'success')
            return redirect(url_for('siteadmin.dashboard'))
    except Exception as e:
        flash('Blog not update please try again', 'warning')
        return redirect(url_for('siteadmin.update_blog'))
    return render_template('update_blog.html',all_category_id = global_all_category_no,all_category_name = global_all_category_name,blog=blog)

@siteadmin.route('/delete_blog/<int:id>', methods=['GET','POST'])
@admin_auth
def delete_blog(id):
    try:
        blog = BlogModel.query.get(id)
        db.session.delete(blog)
        db.session.commit()
        flash('Blog deleted successful!', 'success')
        return redirect(url_for('siteadmin.dashboard'))
    except Exception as e:
        flash('blog not delete!', 'info')
        return redirect(url_for('siteadmin.dashboard'))
    

@siteadmin.route('/admin_search', methods=['GET','POST'])
@admin_auth
def admin_search():
    if request.method == 'GET':
        squery = request.args.get('search_query')
        try:
            blog = BlogModel.query.filter(or_(
            BlogModel.writer_name == squery,
            BlogModel.blog_title == squery,
            BlogModel.blog_creation_date == squery,
            BlogModel.blog_read_count == squery,)).all()
            return render_template('home.html', blog=blog)
        except Exception as e:
            return render_template(url_for('siteadmin.dashboard'))

######################Category model admin#################################
@siteadmin.route('/all_category', methods=['GET','POST'])
@admin_auth
def all_category():
    category = CategoryMaster.query.all()
    return render_template('all_category.html',category=category)

@siteadmin.route('/add_category', methods=['GET','POST'])
@admin_auth
def add_category():
    if request.method == "POST":
        try:
            category_name = request.form.get('category_name')
            category = CategoryMaster(category_name=category_name)
            db.session.add(category)
            db.session.commit()
            flash('Category add successful!', 'success')
            return redirect(url_for('siteadmin.add_category'))
        except Exception as e:
            flash('Category not add please try again1', 'danger')
            return redirect(url_for('siteadmin.add_category'))
    return render_template('add_category.html')

@siteadmin.route('/delete_category/<int:id>', methods=['GET','POST'])
@admin_auth
def delete_category(id):
    try:
        category = CategoryMaster.query.get(id)
        db.session.delete(category)
        db.session.commit()
        flash('Category deleted successful!', 'success')
        return redirect(url_for('siteadmin.all_category'))
    except Exception as e:
        flash('Category not delete!', 'info')
        return redirect(url_for('siteadmin.all_category'))
        
@siteadmin.route('/update_category/<int:id>', methods=['GET','POST'])
@admin_auth
def update_category(id):
    cate = CategoryMaster.query.get(id)
    try:
        if request.method == "POST":
            cate.category_name = request.form.get('category_name')
            db.session.commit()
            flash('Category Update successful!', 'success')
            return redirect(url_for('siteadmin.all_category'))
    except Exception as e:
        flash('Category not update please try again', 'warning')
        return redirect(url_for('siteadmin.all_category'))
    return render_template('update_category.html',category=cate)

@siteadmin.route('/category_filte', methods=['GET','POST'])
@admin_auth
def category_filte():
    try:
        if request.method == 'GET':
            cquery = request.args.get('cquery')
            category = CategoryMaster.query.filter(or_(
            CategoryMaster.category_name == cquery,)).all()
            return render_template('all_category.html',category=category)
    except Exception as e:
        flash('Request filter not perform!', 'warning')
        return redirect(url_for('siteadmin.all_category'))
##########################admin comment contact and subcomment################
@siteadmin.route('/blog_comment', methods=['GET','POST'])
@admin_auth
def blog_comment():
    comment = BlogComment.query.all()
    return render_template('blog_comment.html',comment=comment)

@siteadmin.route('/blogcomment_filte', methods=['GET','POST'])
@admin_auth
def blogcomment_filte():
    try:
        if request.method == 'GET':
            bcquery = request.args.get('bcquery')
            comment = BlogComment.query.filter(or_(
            BlogComment.name == bcquery,
            BlogComment.blog_comment_date == bcquery)).all()
            return render_template('blog_comment.html',comment=comment)
    except Exception as e:
        flash('Request filter not perform!', 'warning')
        return redirect(url_for('siteadmin.blog_comment'))
    
@siteadmin.route('/delete_comment/<int:id>', methods=['GET','POST'])
@admin_auth
def delete_comment(id):
    try:
        com = BlogComment.query.get(id)
        db.session.delete(com)
        db.session.commit()
        flash('Comment deleted successful!', 'success')
        return redirect(url_for('siteadmin.blog_comment'))
    except Exception as e:
        flash('Comment not delete!', 'info')
        return redirect(url_for('siteadmin.blog_comment'))
    

@siteadmin.route('/sub_comment', methods=['GET','POST'])
@admin_auth
def sub_comment():
    subcomment = SubComment.query.all()
    return render_template('sub_comment.html',subcomment=subcomment)

@siteadmin.route('/subcomment_filte', methods=['GET','POST'])
@admin_auth
def subcomment_filte():
    try:
        if request.method == 'GET':
            scquery = request.args.get('scquery')
            subcomment = SubComment.query.filter(or_(
            SubComment.name == scquery,
            SubComment.blog_comment_date == scquery)).all()
            return render_template('sub_comment.html',subcomment=subcomment)
    except Exception as e:
        flash('Request filter not perform!', 'warning')
        return redirect(url_for('siteadmin.sub_comment'))
    
@siteadmin.route('/delete_subcomment/<int:id>', methods=['GET','POST'])
@admin_auth
def delete_subcomment(id):
    try:
        subcom = sub_comment.query.get(id)
        db.session.delete(subcom)
        db.session.commit()
        flash('Comment deleted successful!', 'success')
        return redirect(url_for('siteadmin.sub_comment'))
    except Exception as e:
        flash('Comment not delete!', 'info')
        return redirect(url_for('siteadmin.sub_comment'))
    

@siteadmin.route('/contact_ad', methods=['GET','POST'])
@admin_auth
def contact_ad():
    contact = ContactModel.query.all()
    return render_template('contact_ad.html',contact=contact)

@siteadmin.route('/contact_filte', methods=['GET','POST'])
@admin_auth
def contact_filte():
    try:
        if request.method == 'GET':
            query = request.args.get('query')
            contact = ContactModel.query.filter(or_(
            ContactModel.fullname == query,
            SubComment.email == query)).all()
            return render_template('contact_ad.html',contact=contact)
    except Exception as e:
        flash('Request filter not perform!', 'warning')
        return redirect(url_for('siteadmin.contact_ad'))
    
@siteadmin.route('/delete_contact/<int:id>', methods=['GET','POST'])
@admin_auth
def delete_contact(id):
    try:
        contact = ContactModel.query.get(id)
        db.session.delete(contact)
        db.session.commit()
        flash('Contact deleted successful!', 'success')
        return redirect(url_for('siteadmin.contact_ad'))
    except Exception as e:
        flash('Contact not delete!', 'info')
        return redirect(url_for('siteadmin.contact_ad'))