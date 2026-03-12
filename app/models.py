from datetime import datetime, UTC

from app import db


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    is_completed = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC)
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    @staticmethod
    def validate_data(title, description):
        errors = []
        clean_title = (title or "").strip()
        clean_description = (description or "").strip()

        if not clean_title:
            errors.append("Title is required.")
        if len(clean_title) > 120:
            errors.append("Title must be 120 characters or fewer.")
        if len(clean_description) > 500:
            errors.append("Description must be 500 characters or fewer.")

        return errors
