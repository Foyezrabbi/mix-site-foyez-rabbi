"""
Admin Form
"""

from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import(
    DataRequired, InputRequired, Email, Length, EqualTo,
    ValidationError
)
from wtforms import StringField, SelectField, PasswordField, SubmitField

from .models import Role, User


class LoginForm(FlaskForm):
    email = StringField(
        'Adresse Email',
        validators=[
            DataRequired(), InputRequired(),
            Email(message='Entrer une adresse email valide.')
        ]
    )
    password = PasswordField(
        'Mot de passe',
        validators=[DataRequired("Mot de passe incorrecte !")]
    )
    submit = SubmitField('Se connecter')


class RegistrationForm(FlaskForm):

    email = StringField(
        'Adresse Email',
        validators=[
            DataRequired(), InputRequired(),
            Email(message='Entrer une adresse email valide.')
        ]
    )
    password = PasswordField(
        'Mot de passe',
        validators=[
            InputRequired(),
            Length(
                min=6, max=18,
                message='Choisissez un mot de passe plus fort.'
            )
        ]
    )
    confirm_password = PasswordField(
        'Confirmer le mot de passe',
        validators=[
            InputRequired(),
            EqualTo(
                'password',
                message='Les deux mots de passe ne correspondent pas.'
            ),
        ]
    )
    submit = SubmitField("Inscription")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.lower()).first()
        if user:
            raise ValidationError(
                f"""
                Cet adresse '{email.data.lower()}' est déjà utilisé.
                Veuillez choisir un autre nom !
                """
            )


class UpdateProfileForm(FlaskForm):
    role = SelectField('Role', coerce=int)
    email = StringField(
        'Adresse Email',
        validators=[
            DataRequired(),
            Email(message='Entrer une adresse email valide.')
        ]
    )
    submit = SubmitField("Mettre à jour mon compte")

    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]

    def validate_email(self, email):
        if(
            email.data != current_user.email
            and User.query.filter_by(email=email.data.lower()).first()
        ):
            raise ValidationError(
                f"""
                    Cet adresse '{email.data.lower()}' est déjà utilisé.
                    Veuillez choisir un autre nom !
                """
            )


class ForgotPasswordForm(FlaskForm):
    email = StringField(
        'Adresse Email',
        validators=[
            DataRequired(),
            InputRequired(),
            Email(message='Entrer une adresse email valide.')
        ]
    )
    submit = SubmitField('Envoyer le lien de réinitialisation')

    def validate_email(self, email):
        email_data = email.data.lower()
        user = User.query.filter_by(email=email_data).first()
        if user is None:
            raise ValidationError(
                f"""
                Il n'y a pas de compte avec cet email '{email_data}'.
                Veuillez-vous inscrire.
                """
            )


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        'Mot de passe',
        validators=[
            InputRequired(),
            Length(
                min=6, max=18,
                message='Choisissez un mot de passe plus fort.'
            )
        ]
    )
    confirm_password = PasswordField(
        'Confirmer le mot de passe',
        validators=[
            InputRequired(),
            EqualTo(
                'password',
                message='Les deux mots de passe ne correspondent pas.'
            ),
        ]
    )
    submit = SubmitField('Modifier de mot de passe')
