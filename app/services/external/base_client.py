import asyncio
from enum import Enum
from typing import Any, Optional, Union

import httpx
import tenacity
from fastapi import HTTPException, status
from typing_extensions import TypeAlias

from app.core.config import settings

TIMEOUT = 5  # 5 seconds
RETRIES = 2
WAIT_TO_RETRY = 0.1  # 100 ms


class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


# Types
QueryParams: TypeAlias = dict[str, Any]
Headers: TypeAlias = dict[str, Any]


def _exception_is_service_unavailable(exc: HTTPException) -> bool:
    return exc.status_code == status.HTTP_503_SERVICE_UNAVAILABLE


@tenacity.retry(
    reraise=True,  # raise `HttpException` instead of `RetryError`
    # type: ignore
    retry=tenacity.retry_if_exception(_exception_is_service_unavailable),
    stop=tenacity.stop_after_attempt(RETRIES),
    wait=tenacity.wait_fixed(WAIT_TO_RETRY),
)
async def _request_resource(
    method: str,
    client: httpx.AsyncClient,
    url: str,
    service_name: str,
    *,
    json: Any = None,
    params: Optional[QueryParams] = None,
    headers: Optional[Headers] = None,
    timeout: float = TIMEOUT,
) -> Any:
    # convert headers to str
    if headers:
        headers = {k: str(v) for k, v in headers.items()}

    try:
        response = await client.request(
            method, url, json=json, params=params, headers=headers, timeout=timeout
        )
        response.raise_for_status()
    except httpx.RequestError as e:
        if settings.HTTP_CLIENT_HIDE_INTERNAL_INFO:
            error_msg = f"Failed to contact {service_name}"
        else:
            error_msg = f"An error occurred while requesting {e.request.url!r}"

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"error": error_msg},
        )
    except httpx.HTTPStatusError as e:
        if settings.HTTP_CLIENT_HIDE_INTERNAL_INFO:
            error_msg = f"Error while requesting resource at {service_name}"
        else:
            error_msg = (
                f"Error response while requesting {e.request.url!r} with method: "
                f"{e.request.method} and response: {e.response.text}"
            )

        raise HTTPException(
            status_code=e.response.status_code,
            detail={"error": error_msg},
        )

    resource = response.json()

    return resource


async def request_resource(
    method: HTTPMethod,
    url: str,
    service_name: str,
    *,
    json: Any = None,
    params: Optional[QueryParams] = None,
    headers: Optional[Headers] = None,
    timeout: float = TIMEOUT,
    retries: int = RETRIES,
) -> Any:
    transport = httpx.AsyncHTTPTransport(retries=retries)

    async with httpx.AsyncClient(transport=transport) as client:
        resource = await _request_resource(
            method.value,
            client,
            url,
            service_name,
            json=json,
            params=params,
            headers=headers,
            timeout=timeout,
        )

    return resource


async def bulk_request_resources(
    method: HTTPMethod,
    urls: list[str],
    service_name: str,
    *,
    json: Any = None,
    params: Union[Optional[QueryParams], list[Optional[QueryParams]]] = None,
    headers: Optional[Headers] = None,
    timeout: float = TIMEOUT,
    retries: int = RETRIES,
) -> list:
    transport = httpx.AsyncHTTPTransport(retries=retries)

    if not isinstance(params, list):
        params = [params] * len(urls)

    async with httpx.AsyncClient(transport=transport) as client:
        tasks = [
            _request_resource(
                method.value,
                client,
                url,
                service_name,
                json=json,
                params=param,
                headers=headers,
                timeout=timeout,
            )
            for url, param in zip(urls, params)
        ]
        resources = await asyncio.gather(*tasks)

    return resources
