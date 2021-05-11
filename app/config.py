import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "elysia"
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "elysia"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_ECHO = False
    DEBUG = False


class LocalConfig(Config):
    os.environ["FLASK_ENV"] = "local"
    SQLALCHEMY_ECHO = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        "postgresql+psycopg2://postgres:password@localhost:5432/elysia"
    )


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("TEST_DATABASE_URL") or "sqlite:///:memory:"
    )

    WTF_CSRF_ENABLED = False


config = dict(
    default=LocalConfig,
    local=LocalConfig,
    testing=TestConfig,
)
