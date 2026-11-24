import os
import tempfile

# Banco temporário: os testes nunca tocam em instance/app.db.
# Precisa ser definido ANTES de importar database/app.
_dir = tempfile.mkdtemp(prefix="classflow_test_")
os.environ["DATABASE_URL"] = "sqlite:///" + os.path.join(_dir, "test.db").replace("\\", "/")

import pytest

import models  # noqa: F401  (registra as tabelas)
from database import Base, engine
from app import create_app

Base.metadata.create_all(bind=engine)


@pytest.fixture
def app():
    app = create_app()
    app.config.update({"TESTING": True})
    yield app


@pytest.fixture
def client(app):
    return app.test_client()
