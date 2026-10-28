from app.model.user import User


def test_user_set_and_check_password():
    user = User(username="testuser", email="test@example.com")
    user.set_password("secret123")

    assert user.password_hash != "secret123"
    assert user.check_password("secret123") is True
    assert user.check_password("wrongpassword") is False


def test_user_model_attributes(app, db):
    user = User(username="alice", email="alice@example.com")
    user.set_password("mypassword")
    db.session.add(user)
    db.session.commit()

    saved = db.session.get(User, user.id)
    assert saved is not None
    assert saved.username == "alice"
    assert saved.email == "alice@example.com"
    assert saved.created_at is not None
