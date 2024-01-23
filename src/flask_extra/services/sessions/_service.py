from __future__ import annotations

from attr import define
from flask_super.decorators import service
from sqlalchemy.orm import scoped_session
from svcs import Container

from flask_extra.services.auth import AuthService

from ._models import SessionRepository

_marker = object()


@service
@define
class SessionService:
    auth_service: AuthService
    db_session: scoped_session

    @classmethod
    def svcs_factory(cls, ctn: Container) -> SessionService:
        return cls(
            auth_service=ctn.get(AuthService),
            db_session=ctn.get(scoped_session),
        )

    def get(self, key, default=_marker):
        """Get a value from the user's session by key."""
        user = self.auth_service.get_user()

        repo = SessionRepository(session=self.db_session)
        session = repo.get_one_or_none(user_id=user.id)

        if not session:
            if default is _marker:
                raise KeyError(key)
            return default

        return session.get(key, default)

    def set(self, key, value):
        """Set a value in the user's session by key."""
        repo = SessionRepository(session=self.db_session)

        user = self.auth_service.get_user()
        session, _created = repo.get_or_upsert(user_id=user.id)
        session.set(key, value)
        repo.add(session, auto_commit=True)
