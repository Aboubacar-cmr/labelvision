from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField

class UploadForm(FlaskForm):
    file = FileField('Télécharger une image', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'], 'Seulement des images!')])
    submit = SubmitField('Prédire')
