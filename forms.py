from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Regexp, URL

class LoginForm(FlaskForm):
    playlist = StringField('Playlist:', validators=[URL()])
    submit = SubmitField('Add playlist')