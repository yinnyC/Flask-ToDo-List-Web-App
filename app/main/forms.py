from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL, optional
from app.models import TaskBoard, Task, TaskStatus


class TaskBoardForm(FlaskForm):
    """Form for adding/updating a TaskBoard."""

    title = StringField(
        "Board Title", validators=[DataRequired(), Length(min=3, max=80)]
    )
    submit = SubmitField("Submit")


class TaskForm(FlaskForm):
    """Form for adding/updating a Task."""

    title = StringField(
        "Task Title", validators=[DataRequired(), Length(min=3, max=80)]
    )
    description = TextAreaField("Task Description")
    status = SelectField("Category", choices=TaskStatus.choices())
    due_date = DateField("Due Date")
    submit = SubmitField("Submit")
