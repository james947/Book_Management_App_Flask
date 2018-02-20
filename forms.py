#forms module
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, SubmitField, TextAreaField
#Authenticates the user to the list
class SignupForm(FlaskForm):

    #username variable
    username = StringField('username',[
        validators.data_required(),
        validators.length(min=4 ,max=10)

    ] )

    #emailvariable
    email = StringField('email',[
        validators.data_required(),
        validators.regexp(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                flags=0, message="Invalid email address"
            )

    ] )

    #password Variable
    password = PasswordField('password', [
        validators.data_required(),
        validators.length(min=8, message="The minimun required lenght is 8"),
    ])

    #submit variable
    submit = SubmitField("submit")

#class to validate login
class LoginForm(FlaskForm):
 #auhenticate email
    email = StringField('email', [
        validators.data_required(),
        validators.email(message="invalid email adress"),
        validators.regexp( r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", message="Invalid email address"
        )  
    ])

  #auth password
    password =PasswordField('password',[validators.data_required()])
    #pass login
    login = SubmitField('login')