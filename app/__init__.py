import logging

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect


db = SQLAlchemy()
csrf = CSRFProtect()


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_object("config.Config")
    else:
        app.config.update(test_config)

    db.init_app(app)
    csrf.init_app(app)

    # Include timestamps in log output for easier debugging.
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    from app.routes import bp

    app.register_blueprint(bp)

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_error(_error):
        db.session.rollback()
        return render_template("500.html"), 500

    with app.app_context():
        db.create_all()

    return app
