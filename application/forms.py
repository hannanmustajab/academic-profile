from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, SubmitField, TextAreaField,SelectField
from wtforms.validators import DataRequired, Length


class researchScholarsForm(FlaskForm):
    name = StringField('Full Name',
                       validators=[DataRequired(), Length(min=2, max=20)])
    designation = StringField('Designation',
                              validators=[DataRequired(), Length(min=2, max=20)])
    bio = TextAreaField('Bio',
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


"""
Add New Projects Form
"""

class addProjects(FlaskForm):
    title = StringField('Title',
                       validators=[DataRequired(), Length(min=2, max=50)])
    type = SelectField('Type of projects',choices=[('None', 'Select'),('Research_Project','Research Project'),('Industrial_Project','Industrial Project'),('Book','Book'),('Conference','Conference'),('Publication','Publication')])
    location = TextAreaField('Location', validators=[DataRequired(), Length(min=2, max=20)])
    year = StringField('Date',validators=[DataRequired(), Length(min=2, max=20)])
    link = StringField('URL',validators=[DataRequired(), Length(min=2, max=20)])


    submit = SubmitField('Submit')
