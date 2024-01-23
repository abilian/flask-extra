from __future__ import annotations

import json

from advanced_alchemy.base import BigIntBase
from sqlalchemy.orm import Mapped, mapped_column

from flask_extra.sqla.repository import Repository


class Session(BigIntBase):
    __tablename__ = "ses_session"  # type: ignore
    """Model for storing user server-side sessions."""

    user_id: Mapped[int] = mapped_column(nullable=True, index=True)
    _data: Mapped[str] = mapped_column(nullable=True)

    def get(self, key, default=None):
        data = json.loads(self._data or "{}")
        return data.get(key, default)

    def set(self, key, value):
        data = json.loads(self._data or "{}")
        data[key] = value
        self._data = json.dumps(data)


class SessionRepository(Repository[Session]):
    model_type = Session
