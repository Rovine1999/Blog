from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import UpdateProfile,BlogForm,CommentForm
from ..models import User,Blog,Comment
from ..requests import getQuotes
from flask_login import login_required,current_user
from .. import db,photos
import markdown2

@main.route('/')
def index():
    getquote = getQuotes()
    

    '''
    View root page function that returns the index page and its data
    '''


    title = 'Home - blog website'
    message= "Welcome to Blog Application!!"
     

    return render_template('index.html', title = title,message = message, getquote= getquote)



@main.route('/user/<uname>')
def profile(uname):
     
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
     
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form = form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    get_quote() 
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/blogger/<uname>/update/pic',methods= ['POST'])
@login_required
def update_blogger_pic(uname): 
    blogger = Blogger.query.filter_by(blogger_name = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        Blogger.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/blog/', methods = ['GET','POST'])
@login_required
def new_blog():
    

    form = BlogForm()
    getquote = getQuotes()


    if form.validate_on_submit():
        blog= form.description.data
        title=form.blog_title.data

        # Updated blog instance
        new_blog = blog(blog_title=title,description= blog,user_id=current_user.id)

        title='New blog'
        
        new_blog.save_blog()

        return redirect(url_for('main.new_blog'))

    return render_template('new_blog.html',form= form,getquote= getquote)

@main.route('/blog/blogs', methods=['GET', 'POST'])
@login_required
def all():
    blogs = Blog.query.all()
   
    return render_template('blog.html', blogs=blogs)

@main.route('/comments/<id>' )
@login_required
def comment(id):
    '''
    function to return the comments
    '''
   
    comm =Comment.get_comments(id)
    title = 'comments'
    return render_template('comments.html',comm = comment,title = title)

@main.route('/new_comment/<int:blog_id>', methods = ['GET','POST'])
@login_required
def new_comment(blog_id):

    blogs = Blog.query.filter_by(id = blog_id).first()
    form = CommentForm()

    if form.validate_on_submit():
        comment = form.comment.data

        new_comment = Comment(comment=comment,user_id=current_user.id, blog_id=blog_id)

        new_comment.save_comment()

        return redirect(url_for('main.index'))
    title='New blog'
    return render_template('new_comment.html',title=title,comment_form = form,blog_id=blog_id)

@main.route('/view/<int:id>', methods=['GET', 'POST'])
@login_required
def view(id):
    blog = Blog.query.get_or_404(id)
    blog_comments = Comment.query.filter_by(blog_id=id).all()
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        new_comment = Comment(blog_id=id, comment=comment_form.comment.data, username=current_user)
        new_comment.save_comment()

    return render_template('view.html', blog=blog, blog_comments=blog_comments, comment_form=comment_form)


@main.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    blog = Blog.query.get_or_404(id)
    if blog.user != current_user:
        abort(403)
    db.session.delete(blog)
    db.session.commit()
 
    return redirect(url_for('main.blog'))