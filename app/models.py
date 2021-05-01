"""Create database models to represent tables."""
from app import db
from sqlalchemy.orm import backref
from flask_login import UserMixin
import enum


class FormEnum(enum.Enum):
    """Helper class to make it easier to use enums with forms."""

    @classmethod
    def choices(cls):
        return [(choice.name, choice) for choice in cls]

    def __str__(self):
        return str(self.value)


class TaskStatus(FormEnum):
    BACKLOG = "BACKLOG"
    IN_PROGRESS = "IN_PROGRESS"
    ARCHIVED = "ARCHIVED"
    ICEBOX = "ICEBOX"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    boards = db.relationship("TaskBoard", back_populates="user")

    def __repr__(self):
        return f"<User: {self.username}>"


class TaskBoard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)

    tasks = db.relationship("Task", back_populates="board")

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="boards")

    def __repr__(self):
        return f"<TaskBoard: {self.title}>"


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))
    status = db.Column(db.Enum(TaskStatus), default=TaskStatus.BACKLOG)
    due_date = db.Column(db.Date)
    board_id = db.Column(db.Integer, db.ForeignKey("task_board.id"), nullable=False)
    board = db.relationship("TaskBoard", back_populates="tasks")

    def __repr__(self):
        return f"<Task: {self.title}>"
