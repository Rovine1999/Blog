from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Required,Email,EqualTo,ValidationError
from ..models import User,Blogger
from wtforms import StringField,PasswordField,BooleanField,SubmitField


class RegistrationForm(FlaskForm):
    email = StringField('Your Email Address',validators=[Required(),Email()])
    username = StringField('Enter your username',validators = [Required()])
    password = PasswordField('Password',validators = [Required(), EqualTo('password_confirm',message = 'Passwords must match')])
    password_confirm = PasswordField('Confirm Passwords',validators = [Required()])
    submit = SubmitField('Sign Up')

    def validate_email(self,data_field):
        if User.query.filter_by(email =data_field.data).first():
            raise ValidationError('There is an account with that email')

    def validate_username(self,data_field):
        if User.query.filter_by(username = data_field.data).first():
            raise ValidationError('That username is taken')
        
class BloggerRegistrationForm(FlaskForm):
    blogger_email = StringField('Your Email Address',validators=[Required(),Email()])
    blogger_name = StringField('Enter your username',validators = [Required()])
    blogger_password = PasswordField('Password',validators = [Required(), EqualTo('password_confirm',message = 'Passwords must match')])
    password_confirm = PasswordField('Confirm Passwords',validators = [Required()])
    submit = SubmitField('Blogger Sign Up')

    def validate_email(self,data_field):
        if Blogger.query.filter_by(blogger_email =data_field.data).first():
            raise ValidationError('There is an account with that email')

    def validate_username(self,data_field):
        if Blogger.query.filter_by(blogger_name = data_field.data).first():
            raise ValidationError('That writer name is taken')

class LoginForm(FlaskForm):
    email = StringField('Your Email Address',validators=[Required(),Email()])
    password = PasswordField('Password',validators =[Required()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')
    
class BloggerLoginForm(FlaskForm):
    blogger_email = StringField('Blogger Email Address',validators=[Required(),Email()])
    password = PasswordField('Blogger Password',validators =[Required()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')
