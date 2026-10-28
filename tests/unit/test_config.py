from config import Config, TestingConfig, config


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
