import pytest

from config import Config, ProductionConfig, TestingConfig, config, validate_secret_key


def test_testing_config():
    assert TestingConfig.TESTING is True
    assert TestingConfig.SQLALCHEMY_DATABASE_URI == "sqlite:///:memory:"
    assert TestingConfig.SQLALCHEMY_TRACK_MODIFICATIONS is False


def test_config_registry():
    assert "testing" in config
    assert config["testing"] is TestingConfig
    assert "development" in config
    assert "production" in config
    assert "default" in config


def test_config_defaults_and_types():
    assert isinstance(Config.JWT_EXPIRY_MINUTES, int)
    assert Config.JWT_ALGORITHM == "HS256"
    assert Config.SECRET_KEY is not None
    assert Config.JWT_KEY is not None


def test_validate_secret_key_success():
    valid_key = "a" * 32
    assert validate_secret_key(valid_key) == valid_key


def test_validate_secret_key_too_short():
    with pytest.raises(ValueError, match="at least 32 characters"):
        validate_secret_key("too-short-key")


def test_validate_secret_key_insecure_placeholder():
    with pytest.raises(ValueError, match="Insecure placeholder"):
        validate_secret_key("your-secret-key-here" + "x" * 20)  # length >= 32 but check exact
    with pytest.raises(ValueError, match="Insecure placeholder"):
        validate_secret_key("change-me-in-production")


def test_production_config_validation(monkeypatch):
    monkeypatch.setattr(ProductionConfig, "SECRET_KEY", "insecure")
    with pytest.raises(ValueError):
        ProductionConfig.validate()

    monkeypatch.setattr(ProductionConfig, "SECRET_KEY", "a" * 32)
    monkeypatch.setattr(ProductionConfig, "JWT_KEY", "b" * 32)
    ProductionConfig.validate()  # should not raise
