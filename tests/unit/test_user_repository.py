from app.repository.user_repository import UserRepository


def test_user_repository_create_and_find(app, db):
    user = UserRepository.create("john", "john@example.com", "pass123")

    assert user.id is not None
    assert user.username == "john"
    assert user.email == "john@example.com"
    assert user.check_password("pass123") is True

    by_email = UserRepository.get_by_email("john@example.com")
    assert by_email is not None
    assert by_email.id == user.id

    by_username = UserRepository.get_by_username("john")
    assert by_username is not None
    assert by_username.id == user.id

    assert UserRepository.get_by_email("nonexistent@example.com") is None
    assert UserRepository.get_by_username("nonexistent") is None


def test_user_repository_update_and_delete(app, db):
    user = UserRepository.create("jane", "jane@example.com", "pass456")

    # Update
    user.username = "jane_updated"
    user.set_password("newpass789")
    UserRepository.save(user)

    updated = UserRepository.get_by_id(user.id)
    assert updated.username == "jane_updated"
    assert updated.check_password("newpass789") is True

    # Delete
    UserRepository.delete(user)
    assert UserRepository.get_by_id(user.id) is None
    assert UserRepository.get_by_username("jane_updated") is None
