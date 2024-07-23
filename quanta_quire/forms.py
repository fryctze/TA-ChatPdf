from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired, Length


class UploadForm(FlaskForm):
  document = FileField('Upload Dokumen', validators=[FileRequired(), FileAllowed(['pdf'])])
  submit = SubmitField()


class ChatForm(FlaskForm):
  message = StringField('Name', validators=[DataRequired(), Length(1, 100)])
  submit = SubmitField()
