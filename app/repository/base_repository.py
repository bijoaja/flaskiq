from app import db


class BaseRepository:
    """Base repository — the only layer allowed to call db.session directly."""

    model = None

    @classmethod
    def get_by_id(cls, record_id: int):
        return db.session.get(cls.model, record_id)

    @classmethod
    def get_all(cls) -> list:
        return cls.model.query.all()

    @classmethod
    def save(cls, instance) -> None:
        db.session.add(instance)
        db.session.commit()

    @classmethod
    def delete(cls, instance) -> None:
        db.session.delete(instance)
        db.session.commit()
