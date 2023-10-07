from typing import Union

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.service import get_usuario_service
from app.schemas.usuario import (
    CreateUsuarioPayload,
    EUSerField,
    UpdateUsuarioPayload,
    UsuarioSchema,
)
from app.services.usuario import UsuarioService

router = APIRouter()


@router.get("/list/")
async def get_users_list(
    usuario_service: UsuarioService = Depends(get_usuario_service),
) -> list[UsuarioSchema]:
    users = await usuario_service.get_users_list()

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Usuarios no encontrados"},
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

    update_user = await usuario_service.update_user(field, value, payload)

    if not update_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "El usuario no fue actualizado"},
        )

    return update_user
