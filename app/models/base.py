from collections import defaultdict
import random

# from sqlalchemy import Integer
# from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.schema import MetaData
from sqlalchemy.sql import Delete, Insert, Update

from app.core.config import Settings

settings = Settings()

TICKETS_MODELS_ECHO_QUERIES = getattr(settings, "TICKETS_MODELS_ECHO_QUERIES", False)

engines = defaultdict(list)
engines["main"] = create_async_engine(
    settings.TICKETS_API_DATABASE_URL,
    pool_pre_ping=True,
    echo=TICKETS_MODELS_ECHO_QUERIES,
)


if settings.TICKETS_API_DATABASE_ROUTING_CONFIG:
    engines["leader"] = create_async_engine(
        settings.TICKETS_API_DATABASE_ROUTING_CONFIG.leader,
        pool_pre_ping=True,
        echo=TICKETS_MODELS_ECHO_QUERIES,
    )

    for (
        follower_database_url
    ) in settings.TICKETS_API_DATABASE_ROUTING_CONFIG.followers:
        engines["followers"].append(
            create_async_engine(
                follower_database_url,
                pool_pre_ping=True,
                echo=TICKETS_MODELS_ECHO_QUERIES,
            )
        )

class RoutingSession(Session):
    _force_leader = False

    def get_bind(self, mapper=None, clause=None):
        if (
            self._force_leader
            or self._flushing
            or isinstance(clause, (Insert, Update, Delete))
        ):
            # Force using leader when we have written to DB in the same session instance
            #   to avoid immediately reading after that into a replica
            self._force_leader = True
            return engines["leader"].sync_engine
        else:
            return random.choice(engines["followers"]).sync_engine

def get_database_session(force_leader=False):
    if settings.TICKETS_API_DATABASE_ROUTING_CONFIG and not force_leader:
        return sessionmaker(
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
            class_=AsyncSession,
            sync_session_class=RoutingSession,
        )
    else:
        return sessionmaker(
            bind=engines["main"],
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
            class_=AsyncSession,
        )

tickets_metadata = MetaData(schema="tickets")
Base = declarative_base(metadata=tickets_metadata)

# UnsignedInt = Integer()
# UnsignedInt = UnsignedInt.with_variant(INTEGER(unsigned=True), "mysql")
