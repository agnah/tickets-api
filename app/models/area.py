from sqlalchemy import Column, Enum, String, func, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.schemas.area import AreaAsignar


from .base import Base, UnsignedInt


class Area(Base):
    __tablename__ = "area"
    __mapper_args__ = {"eager_defaults": True}

    id = Column(UnsignedInt, autoincrement=True, primary_key=True)

    nombre = Column(Enum(AreaAsignar), nullable=False)

    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_modificacion = Column(
        DateTime, server_default=func.now(), server_onupdate=func.now())
    fecha_eliminacion = Column(DateTime, default=None)


class TareaAreaRelacion(Base):
    __tablename__ = "tarea_area_relacion"
    __mapper_args__ = {"eager_defaults": True}

    id = Column(UnsignedInt, autoincrement=True, primary_key=True)
    tarea = Column(String(256), nullable=False)
    area_id = Column(UnsignedInt, ForeignKey("area.id"), nullable=False)

    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_modificacion = Column(
        DateTime, server_default=func.now(), server_onupdate=func.now())
    fecha_eliminacion = Column(DateTime, default=None)

    area = relationship("Area")
