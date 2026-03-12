from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class TaskForm(FlaskForm):
    title = StringField(
        "Title", validators=[DataRequired(message="Title is required."), Length(max=120)]
    )
    description = TextAreaField("Description", validators=[Length(max=500)])
    is_completed = BooleanField("Completed")
    submit = SubmitField("Save")


class ActionForm(FlaskForm):
    submit = SubmitField("Submit")
