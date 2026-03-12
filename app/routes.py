from flask import Blueprint, flash, redirect, render_template, request, url_for

from app import db
from app.forms import ActionForm, TaskForm
from app.models import Task


bp = Blueprint("main", __name__)


@bp.get("/")
def index():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    action_form = ActionForm()
    return render_template("index.html", tasks=tasks, action_form=action_form)


@bp.get("/tasks/new")
def new_task():
    form = TaskForm()
    return render_template("create_task.html", form=form)


@bp.post("/tasks")
def create_task():
    form = TaskForm()
    if not form.validate_on_submit():
        return render_template("create_task.html", form=form), 400

    model_errors = Task.validate_data(form.title.data, form.description.data)
    if model_errors:
        for error in model_errors:
            form.title.errors.append(error) if "Title" in error else form.description.errors.append(error)
        return render_template("create_task.html", form=form), 400

    task = Task(
        title=form.title.data.strip(),
        description=(form.description.data or "").strip(),
        is_completed=bool(form.is_completed.data),
    )
    db.session.add(task)
    db.session.commit()

    flash("Task created.", "success")
    return redirect(url_for("main.index"))


@bp.get("/tasks/<int:task_id>/edit")
def edit_task(task_id):
    task = db.get_or_404(Task, task_id)
    form = TaskForm(obj=task)
    return render_template("edit_task.html", form=form, task=task)


@bp.post("/tasks/<int:task_id>/update")
def update_task(task_id):
    task = db.get_or_404(Task, task_id)
    form = TaskForm()

    if not form.validate_on_submit():
        return render_template("edit_task.html", form=form, task=task), 400

    model_errors = Task.validate_data(form.title.data, form.description.data)
    if model_errors:
        for error in model_errors:
            form.title.errors.append(error) if "Title" in error else form.description.errors.append(error)
        return render_template("edit_task.html", form=form, task=task), 400

    task.title = form.title.data.strip()
    task.description = (form.description.data or "").strip()
    task.is_completed = bool(form.is_completed.data)
    db.session.commit()

    flash("Task updated.", "success")
    return redirect(url_for("main.index"))


@bp.post("/tasks/<int:task_id>/delete")
def delete_task(task_id):
    task = db.get_or_404(Task, task_id)
    form = ActionForm()

    if not form.validate_on_submit():
        flash("Invalid request.", "error")
        return redirect(request.referrer or url_for("main.index"))

    db.session.delete(task)
    db.session.commit()
    flash("Task deleted.", "success")
    return redirect(url_for("main.index"))


@bp.post("/tasks/<int:task_id>/toggle")
def toggle_task(task_id):
    task = db.get_or_404(Task, task_id)
    form = ActionForm()

    if not form.validate_on_submit():
        flash("Invalid request.", "error")
        return redirect(request.referrer or url_for("main.index"))

    task.is_completed = not task.is_completed
    db.session.commit()
    flash("Task status updated.", "success")
    return redirect(url_for("main.index"))
