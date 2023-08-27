from fastapi import APIRouter, HTTPException, status

from app.schemas.usuario import UserLoginSchema

from app.services.external.login import login_to_activity_directory

router = APIRouter()


@router.post("/login")
async def login_user(
    payload: UserLoginSchema,
):
    response = await login_to_activity_directory(payload)

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            json={"error": "Usuario o contraseña incorrectos"},
        )
    else:
        return response
