import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.dependencies.db import get_db as get_tickets_db
from app.models.base import Base
from main import app


SYNC_SQLALCHEMY_DATABASE_URL = "sqlite://"
ASYNC_SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite://"

sqlalchemy_factories = []

pytest_plugins = ()

@pytest.fixture()
def tmp_db_path(tmp_path):
    return str(tmp_path / "tickets.db")


@pytest.fixture(autouse=True)
def tickets_sync_session(tmp_db_path):
    """
    SQLAlchemy sync test session (Used for factories)
    """

    engine = create_engine(
        SYNC_SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    @event.listens_for(engine, "connect")
    def connect(dbapi_conn, rec):
        dbapi_conn.execute(f"ATTACH DATABASE '{tmp_db_path}' AS tickets")

    SessionLocal = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
    )

    with SessionLocal() as session:
        # Add session to factories
        for sqlalchemy_factory in sqlalchemy_factories:
            sqlalchemy_factory._meta.sqlalchemy_session = session

        yield session

    # Delete the core.db file from disk if it exists
    try:
        os.remove(tmp_db_path)
    except OSError:
        pass


@pytest.fixture
async def tickets_async_session(tmp_db_path):
    """
    Async SQLAlchemy test session.
    """

    engine = create_async_engine(
        ASYNC_SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )

    @event.listens_for(engine.sync_engine, "connect")
    def connect(dbapi_conn, rec):
        dbapi_conn.execute(f"ATTACH DATABASE '{tmp_db_path}' AS tickets")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    SessionLocal = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        class_=AsyncSession,
    )

    async with SessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

        # Delete the tickets.db file from disk if it exists
        try:
            os.remove(tmp_db_path)
        except OSError:
            pass


@pytest.fixture
async def client(tickets_async_session, redis, mongo_client, remove_logger):
    def get_tickets_db_override():
        return tickets_async_session

    def get_mongo_db_override():
        db = mongo_client.tickets
        return db

    def get_redis_override():
        return redis

    app.dependency_overrides[get_tickets_db] = get_tickets_db_override

    yield TestClient(app)

    app.dependency_overrides = {}


@pytest.fixture
def url_for():
    def inner(*args, **kwargs):
        return app.url_path_for(*args, **kwargs)

    return inner
