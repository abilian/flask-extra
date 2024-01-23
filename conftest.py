import contextlib
import os
from collections.abc import Iterator

import pytest
import svcs
from flask import Flask
from flask.ctx import AppContext
from flask.testing import FlaskCliRunner, FlaskClient
from flask_sqlalchemy import SQLAlchemy
from flask_super import scan_package, register_services
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session
from svcs.flask import container, register_value

from flask_extra.services.sessions import Session

class TestConfig:
    SECRET_KEY = "changeme"
    SECURITY_PASSWORD_SALT = "changeme"
    DEBUG = False
    DEBUG_TB_ENABLED = False

    SQLALCHEMY_DATABASE_URI: str

    def __init__(self):
        if db_uri := os.environ.get("TEST_DATABASE_URI"):
            self.SQLALCHEMY_DATABASE_URI = db_uri
        else:
            self.SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


# We usually only create an app once per session.
@pytest.fixture(scope="session")
def app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(TestConfig())

    app = svcs.flask.init_app(app)
    scan_package("flask_extra")
    register_services(app)

    return app


@pytest.fixture()
def app_context(app) -> AppContext:
    with app.app_context() as ctx:
        yield ctx


@pytest.fixture()
def db(app_context: AppContext, app: Flask) -> Iterator[SQLAlchemy]:
    """Return a fresh db for each test."""
    db = SQLAlchemy(app)

    cleanup_db(db)
    Session.metadata.create_all(db.engine)

    register_value(app, scoped_session, db.session)

    yield db

    db.session.remove()
    cleanup_db(db)


@pytest.fixture()
def db_session(db) -> scoped_session:
    return container.get(scoped_session)


@pytest.fixture()
def client(app: Flask, db_session: scoped_session) -> FlaskClient:
    """Return a Web client, used for testing, bound to a DB session."""
    return app.test_client()


@pytest.fixture()
def runner(app: Flask) -> FlaskCliRunner:
    return app.test_cli_runner()


#
# Cleanup utilities
#
def cleanup_db(db: SQLAlchemy) -> None:
    """Drop all the tables, in a way that doesn't raise integrity errors."""

    for table in reversed(db.metadata.sorted_tables):
        with contextlib.suppress(SQLAlchemyError):
            db.session.execute(table.delete())
