from typing import Any

from app import db


class BaseRepository:
    """Base repository — the only layer allowed to call db.session directly."""

    model: Any = None

    @classmethod
    def get_by_id(cls, record_id: int) -> Any:
        return db.session.get(cls.model, record_id)

    @classmethod
    def get_all(cls) -> list[Any]:
        return cls.model.query.all()

    @classmethod
    def save(cls, instance: Any) -> None:
        db.session.add(instance)
        db.session.commit()

    @classmethod
    def delete(cls, instance: Any) -> None:
        db.session.delete(instance)
        db.session.commit()
