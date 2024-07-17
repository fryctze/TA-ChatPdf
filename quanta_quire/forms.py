from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField


class UploadForm(FlaskForm):
  document = FileField('Upload Dokumen', validators=[FileRequired(), FileAllowed(['pdf'])])
  submit = SubmitField()
