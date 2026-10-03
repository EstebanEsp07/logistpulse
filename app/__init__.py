import time

from flask import Flask
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from .config import Config
from .extensions import db


def _wait_for_db(app):
    """Reintenta la conexión hasta que la base de datos esté disponible."""
    retries = app.config["DB_CONNECT_RETRIES"]
    for attempt in range(1, retries + 1):
        try:
            db.session.execute(text("SELECT 1"))
            app.logger.info("Base de datos disponible (intento %s/%s)", attempt, retries)
            return
        except OperationalError:
            db.session.rollback()
            app.logger.warning("BD no disponible (intento %s/%s). Reintentando...", attempt, retries)
            time.sleep(app.config["DB_CONNECT_DELAY"])
    raise RuntimeError("No fue posible conectar con la base de datos")


def create_app(config_overrides=None):
    """Application factory: ensambla Modelo, Vistas y Controladores."""
    app = Flask(__name__, template_folder="views/templates")
    app.config.from_object(Config)
    if config_overrides:
        app.config.update(config_overrides)

    db.init_app(app)

    from .controllers import register_controllers

    register_controllers(app)

    with app.app_context():
        _wait_for_db(app)
        from . import models  # noqa: F401  (registra las entidades)

        db.create_all()
        if app.config["SEED_DATA"]:
            from .seed import seed_if_empty

            seed_if_empty()
    return app
