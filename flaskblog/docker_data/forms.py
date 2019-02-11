from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class LaunchContainer(FlaskForm):
    image = StringField('Image', validators=[DataRequired()])
    command = TextAreaField('Command', validators=[DataRequired()])
    name = StringField('Name')
    submit = SubmitField('Launch')