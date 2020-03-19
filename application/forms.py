from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class researchScholarsForm(FlaskForm):
    name = StringField('Full Name',
                       validators=[DataRequired(), Length(min=2, max=20)])
    designation = StringField('Designation',
                              validators=[DataRequired(), Length(min=2, max=20)])
    bio = StringField('Bio',
                      validators=[DataRequired(), Length(min=2, max=300)])
    specialization = StringField('Interests / Topic',
                                 validators=[DataRequired(), Length(min=2, max=300)])
    photo = FileField(validators=[FileRequired()])

    submit = SubmitField('Add Now')


"""
Login form
"""


class loginForm(FlaskForm):
    username = StringField('Enter Your Username',
                           validators=[DataRequired()])

    password = PasswordField('Enter Password',
                             validators=[DataRequired()])

    submit = SubmitField('Login ')
