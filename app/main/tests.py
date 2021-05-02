import os
import unittest

from datetime import date

from app import app, db, bcrypt
from app.models import User, TaskBoard, Task, TaskStatus

"""
Run these tests with the command:
python -m unittest app.main.tests
"""

#################################################
# Setup
#################################################
def login(client, username, password):
    return client.post(
        "/login", data=dict(username=username, password=password), follow_redirects=True
    )


def logout(client):
    return client.get("/logout", follow_redirects=True)


def create_user():
    # Creates a user with username 'me1' and password of 'password'
    password_hash = bcrypt.generate_password_hash("password").decode("utf-8")
    user = User(username="me1", password=password_hash)
    db.session.add(user)
    db.session.commit()


def create_board_tasks():
    u1 = User.query.get(1)
    b1 = TaskBoard(title="Internships", user=u1)
    db.session.add(b1)
    t1 = Task(
        title="apply Apple SWE intern",
        description="Team SPG",
        status="IN_PROGRESS",
        due_date=date(2021, 5, 1),
        board=b1,
    )
    db.session.add(t1)
    db.session.commit()


#################################################
# Tests
#################################################
class MainTests(unittest.TestCase):
    def setUp(self):
        """Executed prior to each test."""
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_homepage_logged_out(self):
        """Test that the homepage shows right tabs when logged out."""
        # Set up
        create_user()
        # Make a GET request
        response = self.app.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Check that page contains all of the things we expect
        response_text = response.get_data(as_text=True)
        self.assertIn("Log In", response_text)
        self.assertIn("Sign Up", response_text)

    def test_dashboard(self):
        """Test the dashboard shows the right info"""
        create_user()
        create_board_tasks()
        login(self.app, "me1", "password")

        response = self.app.get("/myBoards", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response_text = response.get_data(as_text=True)
        self.assertIn("Internships", response_text)
        self.assertNotIn("Log In", response_text)
        self.assertNotIn("Sign Up", response_text)

    def test_create_board(self):
        """ Test creating a taskboard """
        create_user()
        login(self.app, "me1", "password")

        post_data = {"title": "Homework", "user": User.query.get(1)}
        self.app.post("/new_board", data=post_data)

        created_board = TaskBoard.query.filter_by(title="Homework").one()
        self.assertIsNotNone(created_board)
        self.assertEqual(created_board.title, "Homework")

    def test_create_task(self):
        """ Test creating a task """
        create_user()
        login(self.app, "me1", "password")
        self.app.post(
            "/new_board", data={"title": "Homework", "user": User.query.get(1)}
        )
        board = TaskBoard.query.filter_by(title="Homework").one()
        post_data = {
            "title": "BEW1-2 final project",
            "description": "Should Have Models, Forms, unitest",
            "status": "IN_PROGRESS",
            "due_date": date(2021, 5, 10),
            "board": board,
        }
        self.app.post(f"/new_task/{board.id}", data=post_data)

        created_task = Task.query.filter_by(title="BEW1-2 final project").one()
        self.assertIsNotNone(created_task)
        self.assertEqual(created_task.description, "Should Have Models, Forms, unitest")

    def test_view_task(self):
        """ Test showing the info of tasks """
        create_user()
        create_board_tasks()
        login(self.app, "me1", "password")

        response = self.app.get("/view_tasks/1", follow_redirects=True)

        response_text = response.get_data(as_text=True)
        self.assertIn("apply Apple SWE intern", response_text)
        self.assertIn("Team SPG", response_text)
        self.assertIn("IN_PROGRESS", response_text)
        self.assertIn("2021-05-01", response_text)

    def test_update_board(self):
        """ Test updating taskboard """
        create_user()
        create_board_tasks()
        login(self.app, "me1", "password")
        board = TaskBoard.query.get(1)
        user = User.query.get(1)

        post_data = {"title": "Job Hunting", "user": user}
        self.app.post(f"/update-taskBoard/{board.id}", data=post_data)

        update_board = TaskBoard.query.filter_by(title="Job Hunting").one()
        self.assertIsNotNone(update_board)
        self.assertEqual(update_board.title, "Job Hunting")

    def test_update_task(self):
        """ Test updating task """
        create_user()
        create_board_tasks()
        login(self.app, "me1", "password")
        board = TaskBoard.query.get(1)
        task = Task.query.get(1)
        post_data = {
            "title": "BEW1-2 final project",
            "description": "Should Have Models, Forms, unitest",
            "status": "ARCHIVED",
            "due_date": date(2021, 5, 10),
            "board": board,
        }
        self.app.post(f"/update_task/{board.id}/{task.id}", data=post_data)

        update_task = Task.query.filter_by(title="BEW1-2 final project").one()
        self.assertIsNotNone(update_task)
        self.assertEqual(update_task.status, TaskStatus.ARCHIVED)
