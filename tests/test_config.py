import importlib
import os
import app.config


def test_config(monkeypatch):
    # Имитируем окружение 'production'
    monkeypatch.setenv("FASTAPI_ENV", "production")
    importlib.reload(app.config)
    assert app.config.config.config_type == 'prod'
    assert isinstance(app.config.config, app.config.ProdConfig)

    # Имитируем окружение 'development'
    monkeypatch.setenv("FASTAPI_ENV", "")
    importlib.reload(app.config)
    assert app.config.config.config_type == 'dev'
    assert isinstance(app.config.config, app.config.BaseConfig)

