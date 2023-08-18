from sqlalchemy import Column, Enum, String, func, DateTime

from app.schemas.area import NombreArea


from .base import Base, UnsignedInt


class Area(Base):
    __tablename__ = "area"
    __mapper_args__ = {"eager_defaults": True}

    id = Column(UnsignedInt, autoincrement=True, primary_key=True)

    nombre = Column(Enum(NombreArea), nullable=False)

    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_modificacion = Column(
        DateTime, server_default=func.now(), server_onupdate=func.now())
    fecha_eliminacion = Column(DateTime, default=None)
