from typing import Union


from app.models.usuario import Usuario
from app.schemas.usuario import UserLoginSchema

from .usuario import UsuarioService
from .external.login_external import get_user_from_activity_directory


from .layer import ServiceLayer, register_service


@register_service("Login")
class LoginService(ServiceLayer):
    def user_login(self, payload: UserLoginSchema) -> Union[Usuario, None]:
        repo_usuario = UsuarioService(db=self.db)

        user = repo_usuario.get_user_by_field(field="email", value=payload.email)

        if not user:
            return False

        return get_user_from_activity_directory(payload)

    def logout(self, user: Usuario) -> bool:
        return self.repository.logout(user)
