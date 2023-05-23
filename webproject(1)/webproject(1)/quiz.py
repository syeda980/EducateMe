from flask_wtf import FlaskForm as Form
from wtforms import RadioField
from wtforms.validators import ValidationError
from wtforms.validators import InputRequired
from random import randrange


class CorrectAnswer(object):
    def __init__(self, answer):
        self.answer = answer
def __call__(self, form, field):
    message = 'Incorrect answer.'

    if field.data != self.answer:
        raise ValidationError(message)
class PopQuiz(Form):
    class Meta:
        csrf = ''
    q1 = RadioField(
        "Which of the following is the use of id() function in python?",
        choices=[('Every object doesn’t have a unique id', 'Every object doesn’t have a unique id'),
         ('Id returns the identity of the object','Id returns the identity of the object'),
         ('All of the mentioned','All of the mentioned'),('None of the mentioned','None of the mentioned')],
        validators=[InputRequired(CorrectAnswer('Id returns the identity of the object'))]
        )

    q2 = RadioField(
        "Is Python case sensitive when dealing with identifiers?",
        choices=[('Yes', 'Yes'), ('No', 'No')],
        validators=[InputRequired(CorrectAnswer('Yes'))]
    )

    q3 = RadioField(
        "All keywords in Python are in",
        choices=[('UPPER CASE', 'UPPER CASE'), ('lower case', 'lower case'),('Capitalized', 'Capitalized'),
                 ('None of the mentioned', 'None of the mentioned')],
        validators=[InputRequired(CorrectAnswer('None of the mentioned'))]
    )

    q4 = RadioField(
        "What is the return type of function id?",
        choices=[('float', 'float'), ('bool', 'bool'),('int', 'int'), ('dict', 'dict')],
        validators=[InputRequired(CorrectAnswer('int'))]
    )