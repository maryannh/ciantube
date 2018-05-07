from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, Regexp, URL

class SuggestForm(FlaskForm):
    suggestion = StringField('What would you like to see in CianTube? Fill in your favourite channel or topic:', validators=[DataRequired()])
    submit = SubmitField('Send suggestion')

class AddForm(FlaskForm):
    playlist = StringField('Playlist ID:', validators=[DataRequired()])
    submit = SubmitField('Add playlist')