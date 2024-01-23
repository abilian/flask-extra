from advanced_alchemy import ModelT, SQLAlchemySyncRepository
from sqlalchemy.orm import scoped_session
from svcs.flask import container


class Repository(SQLAlchemySyncRepository[ModelT]):
    """Base class for repositories."""

    @classmethod
    def svcs_factory(cls):
        session = container.get(scoped_session)
        return cls(session=session)
