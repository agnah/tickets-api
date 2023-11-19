from typing import Union

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.dependencies.service import get_usuario_service
from app.schemas.usuario import (
    CreateUsuarioPayload,
    EUSerField,
    RolUsuario,
    UpdateUsuarioPayload,
    UsuarioSchema,
)
from app.services.usuario import UsuarioService

router = APIRouter()


@router.get("/all/")
async def get_all_users(
    usuario_service: UsuarioService = Depends(get_usuario_service),
) -> list[UsuarioSchema]:
    users = await usuario_service.get_all_users()

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Usuarios no encontrados"},
        )

    return users


@router.get("/{area_id}/")
async def get_users_por_area_filtrando_por_rol(
    area_id: int,
    rol: RolUsuario = Query(None, description="Rol del usuario que se desea filtrar"),
    usuario_service: UsuarioService = Depends(get_usuario_service),
) -> list[UsuarioSchema]:
    users = await usuario_service.get_users_list(area_id=area_id, rol=rol)

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error":f"No se encontraron usuarios con ese {rol} para esa el area con id={area_id}"},
        )

    return users


@router.get("/")
async def get_user_by_field(
    field: EUSerField,
    value: Union[str, int],
    usuario_service: UsuarioService = Depends(get_usuario_service),
) -> UsuarioSchema:
    user = await usuario_service.get_user_by_field(field, value)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Usuario no encontrado"},
        )

    return user


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: CreateUsuarioPayload,
    usuario_service: UsuarioService = Depends(get_usuario_service),
) -> UsuarioSchema:
    user = await usuario_service.get_user_by_field(EUSerField.EMAIL, payload.email)

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "El usuario ya existe"},
        )

    new_user = await usuario_service.create_user(payload)

    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "El usuario no fue creado"},
        )

    return new_user


@router.patch("/{field}/{value}")
async def update_user(
    field: EUSerField,
    value: Union[str, int],
    payload: UpdateUsuarioPayload,
    usuario_service: UsuarioService = Depends(get_usuario_service),
) -> UsuarioSchema:
    user = await usuario_service.get_user_by_field(field, value)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Usuario no encontrado"},
        )

    updated_user_id = await usuario_service.update_user(field, value, payload)

    if not updated_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": f"El usuario con id={updated_user_id} no fue actualizado"},
        )

    return updated_user_id
