from urllib.parse import urljoin

from fastapi.encoders import jsonable_encoder

from app.core.config import settings
from app.schemas.usuario import UserLoginSchema
from app.services.external.base_client import HTTPMethod, request_resource

ACTIVITY_DIRECTORY_API_BASE_URL = settings.ACTIVITY_DIRECTORY_API_BASE_URL
# todo: completar nombre del servicio
SERVICE_NAME = "login-api-service"


async def get_user_from_activity_directory(user_id: int, course_id: int):
    # todo: cambiar url del endpoint
    url = urljoin(ACTIVITY_DIRECTORY_API_BASE_URL, "/api/login")

    try:
        user_from_activity_directory = await request_resource(
            HTTPMethod.GET, url, SERVICE_NAME
        )

        return user_from_activity_directory
    except Exception:
        return None


async def login_to_activity_directory(
    payload: UserLoginSchema,
):
    url = urljoin(ACTIVITY_DIRECTORY_API_BASE_URL, "/api/login")

    # headers = {"X-UserId": str(ADMIN_USER_ID)}

    try:
        login_data = await request_resource(
            HTTPMethod.PUT,
            url,
            SERVICE_NAME,
            json=jsonable_encoder(payload),
            # headers=headers,
        )

        return login_data
    except Exception:
        return None
