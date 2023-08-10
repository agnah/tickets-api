from sqlalchemy import Boolean, Column, Enum, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.schemas.usuario import PerfilUsuario, RolUsuario


from .base import Base, UnsignedInt


class Usuario(Base):
    __tablename__ = "usuario"
    __mapper_args__ = {"eager_defaults": True}

    id = Column(UnsignedInt, autoincrement=True, primary_key=True)
    nombre = Column(String(256), nullable=False)
    apellido = Column(String(256), nullable=False)
    email = Column(String(256), nullable=False)
    telefono = Column(String(256), nullable=False)
    perfil = Column(Enum(PerfilUsuario), nullable=False)
    rol = Column(Enum(RolUsuario), nullable=False)

    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_modificacion = Column(
        DateTime, server_default=func.now(), server_onupdate=func.now())
    fecha_eliminacion = Column(DateTime, default=None)
