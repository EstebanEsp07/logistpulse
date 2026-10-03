import os


class Config:
    """Configuración leída desde variables de entorno (ver .env.example)."""

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///logistpulse_dev.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-not-a-secret")
    # Reintentos de conexión a la BD (la app espera a que PostgreSQL esté listo)
    DB_CONNECT_RETRIES = int(os.getenv("DB_CONNECT_RETRIES", "15"))
    DB_CONNECT_DELAY = float(os.getenv("DB_CONNECT_DELAY", "2"))
    SEED_DATA = os.getenv("SEED_DATA", "true").lower() == "true"
