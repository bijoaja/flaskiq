from app.repository.base_repository import BaseRepository
from app.model.user import User


class UserRepository(BaseRepository):
    model = User

    @classmethod
    def get_by_email(cls, email: str):
        return User.query.filter_by(email=email).first()

    @classmethod
    def get_by_username(cls, username: str):
        return User.query.filter_by(username=username).first()

    @classmethod
    def create(cls, username: str, email: str, password: str) -> User:
        user = User(username=username, email=email)
        user.set_password(password)
        cls.save(user)
        return user
