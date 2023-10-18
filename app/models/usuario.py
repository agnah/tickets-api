from sqlalchemy import Column, Enum, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.schemas.ticket import ESede

# from app.schemas.ticket import ESede

# from app.schemas.ticket import ESede

from app.schemas.usuario import PerfilUsuario, RolUsuario


from .base import Base, UnsignedInt


class Usuario(Base):
    __tablename__ = "usuario"
    __mapper_args__ = {"eager_defaults": True}

    id = Column(UnsignedInt, autoincrement=True, primary_key=True)
    token = Column(String(256), nullable=False)

    nombre = Column(String(256), nullable=False)
    apellido = Column(String(256), nullable=False)
    email = Column(String(256), nullable=False)
    celular = Column(String(256), nullable=True)
    telefono = Column(String(256), nullable=True)
    interno = Column(String(256), nullable=True)

    area_id = Column(UnsignedInt, ForeignKey("area.id"))
    # TODO: Completar una vez que nos pasen los datos
    sede = Column(Enum(ESede), nullable=False, default=ESede.NUEVE_DE_JULIO)
    piso = Column(String(256), nullable=True)

    perfil = Column(Enum(PerfilUsuario))
    rol = Column(Enum(RolUsuario))

    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_modificacion = Column(
        DateTime, server_default=func.now(), server_onupdate=func.now()
    )
    fecha_eliminacion = Column(DateTime, default=None)

    area = relationship("Area")
