from fastapi import APIRouter, HTTPException, status, Depends
from app.dependencies.service import get_usuario_service, get_login_service

from app.schemas.usuario import UserLoginSchema, EUSerField

from app.services.login import LoginService
from app.services.usuario import UsuarioService

router = APIRouter()


@router.post("/login")
async def login_user(
    payload: UserLoginSchema,
    user_service: UsuarioService = Depends(get_usuario_service),
    login_service: LoginService = Depends(get_login_service),
):
    user = await user_service.get_user_by_field(EUSerField.EMAIL, payload.email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            json={"error": "Usuario inexistente"},
        )

    access_token = await login_service.user_login(payload)

    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            json={"error": "Usuario o contraseña incorrectos"},
        )

    return {"access_token": access_token, "token_type": "bearer"}
