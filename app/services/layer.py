from functools import partial

from attrs import define

from .base import BaseService

SERVICES_DIRECTORY = {}


def register_service(name: str):
    def decorator(cls):
        SERVICES_DIRECTORY[name] = cls

        def wrapped(*args, **kwargs):
            return cls(*args, **kwargs)

        return wrapped

    return decorator


@define
class ServiceLayer(BaseService):
    def get_service(self, service_name: str, as_partial: bool = False):
        """
        Get a service by their name


        If `as_partial` is True, the service will be returned as a partial application of the class
        """

        if service_name not in SERVICES_DIRECTORY:
            raise Exception(f"Service {service_name} not found")

        service = SERVICES_DIRECTORY[service_name]

        if as_partial:
            return partial(service, db=self.db)

        return service(db=self.db)