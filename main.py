from fastapi import FastAPI

from app.core.config import Settings

from app.endpoints.healthcheck import router as healthcheck_router
from app.endpoints.ticket import router as tickets_router
from app.endpoints.area import router as area_router

app = FastAPI()
setings = Settings()

# Routers
app.include_router(healthcheck_router, prefix="/api/healthcheck", tags=["Healthcheck"])
app.include_router(tickets_router, prefix="/api/tickets", tags=["Tickets"])
app.include_router(area_router, prefix="/api/area", tags=["Area"])
