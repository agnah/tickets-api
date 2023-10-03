from typing import Union
from datetime import datetime, timedelta
from jose import jwt

from app.models.usuario import Usuario
from app.schemas.usuario import UserLoginSchema

from app.services.external.login_external import get_user_from_activity_directory


from app.services.layer import ServiceLayer, register_service

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 600  # 10 hours
SECRECT = "f1af7995c1b0c403b235b689f11b4caf952db856d757ee1b989e07a0b5be9c32"


@register_service("Login")
class LoginService(ServiceLayer):
    async def user_login(self, payload: UserLoginSchema) -> Union[Usuario, None]:
        access_login = get_user_from_activity_directory(payload)

        if not access_login:
            return None

        return await self.generate_jwt(payload.email)

    async def logout(self, user: Usuario) -> bool:
        return self.repository.logout(user)

    async def generate_jwt(self, user_email: str) -> str:
        access_token = {
            "sub": user_email,
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        }

        return jwt.encode(access_token, SECRECT, algorithm=ALGORITHM)
