""" Contact forms"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import InputRequired, DataRequired, Length, Email, Regexp

from .models import Contact

SUBJECT_CHOICE = [
    (1, "I want to make an appointment with you."),
    (2, "I would like more information about your services."),
    (3, "Can I have information about your training sessions ?"),
    (4, "I would like to hire you on a project !"),
]


class ContactForm(FlaskForm):
    fullname = StringField(
        "Your full Name",
        validators=[
            Length(min=4, max=80), InputRequired(),
            DataRequired(),
        ]
    )
    email = StringField(
        'Email Address',
        validators=[
            Length(min=4, max=80), DataRequired(), InputRequired(),
            Email(message='Enter your email Address.')
        ]
    )
    phone = StringField(
        "Phone",
        validators=[
            Length(min=4, max=15), InputRequired(), DataRequired(),
        ]
    )
    subject = SelectField(
        "Topic",
        choices=SUBJECT_CHOICE, coerce=int,
        validators=[InputRequired(), DataRequired()]
    )
    message = TextAreaField("Your message", validators=[InputRequired(), DataRequired()])
    submit = SubmitField("Send the message")
