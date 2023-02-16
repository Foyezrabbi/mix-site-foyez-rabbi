from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField, FileAllowed
from wtforms.validators import InputRequired, DataRequired, Length
from wtforms import StringField, SelectField, TextAreaField, SubmitField

from .models import Category, Project
from flask_ckeditor import CKEditorField


class ProjectForm(FlaskForm):
    category = SelectField('Category', coerce=int)
    name = StringField(
        "Nom du projet", validators=[
            InputRequired(),
            DataRequired()
        ]
    )
    image = FileField(
        "Image du projet",
        validators=[
            FileRequired(),
            FileAllowed(['jpg', 'png', 'jpeg']),
        ]
    )
    submit = SubmitField("Ajouter")

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.category.choices = [(cat.id, cat.name) for cat in Category.query.order_by(Category.name).all()]


class StorieForm(FlaskForm):
    fullname = StringField(
        "Nom & prénoms", validators=[
            InputRequired(),
            DataRequired()
        ]
    )
    status = StringField(
        "Profession", validators=[
            InputRequired(),
            DataRequired()
        ]
    )
    content = CKEditorField(
        "Message ...",
        validators=[
            DataRequired(),
            InputRequired()
        ]
    )
    image = FileField(
        "Photo de profile",
        validators=[
            FileRequired(),
            FileAllowed(['jpg', 'png', 'jpeg']),
        ]
    )
    submit = SubmitField('soumettre')


class ClientForm(FlaskForm):
    name = StringField(
        "Nom de l'entreprise", validators=[
            InputRequired(),
            DataRequired()
        ]
    )
    image = FileField(
        "Image",
        validators=[
            FileRequired(),
            FileAllowed(['jpg', 'png', 'jpeg']),
        ]
    )
    submit = SubmitField('soumettre')
