from __future__ import annotations

import pytest
from flask import g
from svcs.flask import container

from . import SessionService


class FakeUser:
    id = 1


@pytest.mark.usefixtures("db_session")
def test_session() -> None:
    g.user = FakeUser()

    session_service = container.get(SessionService)
    assert session_service.get("foo", None) is None

    session_service.set("foo", "bar")
    assert session_service.get("foo") == "bar"
