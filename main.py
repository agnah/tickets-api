from fastapi import FastAPI

from app.endpoints.healthcheck import router as healthcheck_router
from app.endpoints.login import router as login_router

app = FastAPI()

# Routers
app.include_router(healthcheck_router, prefix="/api/healthcheck", tags=["Healthcheck"])
app.include_router(login_router, prefix="/api", tags=["Login"])
