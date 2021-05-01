from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from app.models import User, TaskBoard, Task
from app.main.forms import TaskBoardForm, TaskForm
from app import app, db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################


@main.route("/")
def homepage():
    return render_template("home.html")


@main.route("/myBoards")
@login_required
def dashboard():
    form = TaskBoardForm()
    all_boards = TaskBoard.query.filter_by(user=current_user)
    return render_template("user_board.html", all_boards=all_boards, form=form)


@main.route("/new_board", methods=["GET", "POST"])
@login_required
def create_board():
    form = TaskBoardForm()
    if form.validate_on_submit():
        new_board = TaskBoard(title=form.title.data, user=current_user)
        db.session.add(new_board)
        db.session.commit()
        flash("New board was created successfully.")
    return redirect(url_for("main.dashboard"))


@main.route("/update-taskBoard/<board_id>", methods=["POST"])
@login_required
def update_board(board_id):
    form = TaskBoardForm()
    if form.validate_on_submit():
        board_to_update = TaskBoard.query.get(board_id)
        board_to_update.title = form.title.data
        db.session.add(board_to_update)
        db.session.commit()
        flash("Task board was updated successfully.")
    return redirect(url_for("main.dashboard"))


@main.route("/view_tasks/<board_id>")
@login_required
def view_tasks(board_id):
    form = TaskForm()
    board = TaskBoard.query.get(board_id)
    all_tasks = Task.query.filter_by(board=board)
    return render_template(
        "task_detail.html",
        all_tasks=all_tasks,
        form=form,
        board_id=board_id,
        board_title=board.title,
    )


@main.route("/new_task/<board_id>", methods=["GET", "POST"])
@login_required
def create_Task(board_id):
    form = TaskForm()
    board = TaskBoard.query.get(board_id)
    if form.validate_on_submit():
        new_task = Task(
            title=form.title.data,
            description=form.description.data,
            status=form.status.data,
            due_date=form.due_date.data,
            board=board,
        )
        db.session.add(new_task)
        db.session.commit()
        flash("New task was created successfully.")
    return redirect(url_for("main.view_tasks", board_id=board_id))


@main.route("/update_task/<board_id>/<task_id>", methods=["POST"])
@login_required
def update_Task(board_id, task_id):
    form = TaskForm()
    task_to_update = Task.query.get(task_id)
    if form.validate_on_submit():
        task_to_update.title = form.title.data
        task_to_update.description = form.description.data
        task_to_update.status = form.status.data
        task_to_update.due_date = form.due_date.data
        db.session.add(task_to_update)
        db.session.commit()
        flash("Task was updated successfully.")
    return redirect(url_for("main.view_tasks", board_id=board_id))
