from __future__ import annotations

from flask import g
from flask_sqlalchemy import SQLAlchemy
from svcs.flask import container

from . import SessionService


class FakeUser:
    id = 1


def test_session(db: SQLAlchemy) -> None:
    g.user = FakeUser()

    session_service = container.get(SessionService)
    assert session_service.get("foo", None) is None

    session_service.set("foo", "bar")
    assert session_service.get("foo") == "bar"
