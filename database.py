import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
import sqlite3

from config import INSTANCE_DIR

os.makedirs(INSTANCE_DIR, exist_ok=True)

_db_path = os.path.join(INSTANCE_DIR, "app.db").replace("\\", "/")
DATABASE_URL = f"sqlite:///{_db_path}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)
@event.listens_for(Engine, "connect")
def ativar_foreign_keys(dbapi_connection, connection_record):

    if isinstance(dbapi_connection, sqlite3.Connection):

        cursor = dbapi_connection.cursor()

        cursor.execute("PRAGMA foreign_keys=ON")

        cursor.close()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
