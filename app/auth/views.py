from . import auth
from flask import render_template,redirect,url_for, flash,request
from flask_login import login_user,logout_user,login_required
from ..models import User,Blogger
from ..requests import getQuotes
from .forms import LoginForm,RegistrationForm,BloggerRegistrationForm,BloggerLoginForm
from .. import db
from ..email import mail_message


@auth.route('/login/user',methods=['GET','POST'])
def login():
    getquote = getQuotes()
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email = login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user,login_form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))

        flash('Invalid username or Password')

    title = "Wanjala blog website"
    return render_template('auth/login.html',login_form = login_form,title=title, getquote= getquote)
@auth.route('/login/blogger',methods=['GET','POST'])
def blogger_login():
    quote = get_quote()
    login_form = BloggerLoginForm()
    if login_form.validate_on_submit():
        blogger = Blogger.query.filter_by(blogger_email = login_form.blogger_email.data).first()
        if blogger is not None and blogger.verify_password(login_form.password.data):
            login_user(blogger,login_form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))

        flash('Invalid username or Password')

    title = "Wanjala"
    return render_template('auth/blogger_login.html',login_form = login_form,title=title, getquote= getquote)

@auth.route('/register',methods = ["GET","POST"])
def register():
    getquote = getQuotes()
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data,password = form.password.data)
        db.session.add(user)
        db.session.commit()

        mail_message("Welcome to Wanjala blog ","email/welcome_user",user.email,user=user)

        return redirect(url_for('auth.login'))
        title = "New Account"
    return render_template('auth/register.html',registration_form = form, getquote= getquote)

@auth.route('/register/blogger',methods = ["GET","POST"])
def blogger_register():
    getquote = getQuotes()
    form = BloggerRegistrationForm()
    if form.validate_on_submit():
        blogger = Blogger(blogger_email = form.blogger_email.data, blogger_name = form.blogger_name.data,password = form.blogger_password.data)
        db.session.add(blogger)
        db.session.commit()

        mail_message("Welcome to Wanjala  blog as a blogger","email/welcome_user",blogger.blogger_email,blogger=blogger)

        return redirect(url_for('auth.blogger_login'))
        title = "New Account"
    return render_template('auth/blogger_register.html',registration_form = form, getquote= getquote)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Congratulations, you have successfully logged out from your account")
    return redirect(url_for("main.index"))