from app import db
from app.models import Task


def create_sample_task(title="Sample Task", description="Sample Description"):
    task = Task(title=title, description=description, is_completed=False)
    db.session.add(task)
    db.session.commit()
    return task


def test_index_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"My Tasks" in response.data


def test_create_task_success(client, app):
    response = client.post(
        "/tasks",
        data={"title": "Buy milk", "description": "2 liters", "is_completed": "y"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Task created." in response.data

    with app.app_context():
        task = Task.query.filter_by(title="Buy milk").first()
        assert task is not None
        assert task.is_completed is True


def test_create_task_validation_error(client):
    response = client.post(
        "/tasks",
        data={"title": "", "description": "desc"},
    )

    assert response.status_code == 400
    assert b"Title is required." in response.data


def test_update_task_success(client, app):
    with app.app_context():
        task = create_sample_task()
        task_id = task.id

    response = client.post(
        f"/tasks/{task_id}/update",
        data={
            "title": "Updated Task",
            "description": "Updated Description",
            "is_completed": "y",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Task updated." in response.data

    with app.app_context():
        updated = db.session.get(Task, task_id)
        assert updated.title == "Updated Task"
        assert updated.description == "Updated Description"
        assert updated.is_completed is True


def test_toggle_task_status(client, app):
    with app.app_context():
        task = create_sample_task()
        task_id = task.id
        assert task.is_completed is False

    response = client.post(f"/tasks/{task_id}/toggle", follow_redirects=True)
    assert response.status_code == 200

    with app.app_context():
        toggled = db.session.get(Task, task_id)
        assert toggled.is_completed is True


def test_delete_task(client, app):
    with app.app_context():
        task = create_sample_task()
        task_id = task.id

    response = client.post(f"/tasks/{task_id}/delete", follow_redirects=True)
    assert response.status_code == 200
    assert b"Task deleted." in response.data

    with app.app_context():
        deleted = db.session.get(Task, task_id)
        assert deleted is None


def test_missing_task_returns_404(client):
    response = client.get("/tasks/9999/edit")
    assert response.status_code == 404
