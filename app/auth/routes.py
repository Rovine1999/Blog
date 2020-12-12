
from . import auth
from flask import render_template,redirect,url_for, flash,request
from flask_login import login_user,logout_user,login_required
from ..models import User,Blogger
from ..request import get_quote
from .forms import LoginForm,RegistrationForm,WriterRegistrationForm,BloggerLoginForm
from .. import db
from ..email import mail_message


@bp.route('/login/user',methods=['GET','POST'])
def login():
    quote = get_quote()
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email = login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user,login_form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))

        flash('Invalid username or Password')

    title = "Wanjala blog website"
    return render_template('auth/login.html',login_form = login_form,title=title, quote=quote)
@bp.route('/login/blogger',methods=['GET','POST'])
def writer_login():
    quote = get_quote()
    login_form = BloggerLoginForm()
    if login_form.validate_on_submit():
        blogger = Writer.query.filter_by(blogger_email = login_form.blogger_email.data).first()
        if blogger is not None and blogger.verify_password(login_form.password.data):
            login_user(blogger,login_form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))

        flash('Invalid username or Password')

    title = "Wanjala"
    return render_template('auth/writer_login.html',login_form = login_form,title=title, quote=quote)

@bp.route('/register',methods = ["GET","POST"])
def register():
    quote = get_quote()
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data,password = form.password.data)
        db.session.add(user)
        db.session.commit()

        mail_message("Welcome to Wanjala blog ","email/welcome_user",user.email,user=user)

        return redirect(url_for('auth.login'))
        title = "New Account"
    return render_template('auth/register.html',registration_form = form, quote=quote)

@bp.route('/register/writer',methods = ["GET","POST"])
def writer_register():
    quote = get_quote()
    form = WriterRegistrationForm()
    if form.validate_on_submit():
        blogger = Writer(blogger_email = form.blogger_email.data, writer_name = form.writer_name.data,password = form.writer_password.data)
        db.session.add(blogger)
        db.session.commit()

        mail_message("Welcome to Wanjala  blog as a blogger","email/welcome_user",blogger.blogger_email,blogger=blogger)

        return redirect(url_for('auth.blogger_login'))
        title = "New Account"
    return render_template('auth/blogger_register.html',registration_form = form, quote=quote)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Congratulations, you have succ")
    return redirect(url_for("main.index"))