from fastapi import FastAPI

from app.endpoints.healthcheck import router as healthcheck_router

app = FastAPI()

# Routers
app.include_router(healthcheck_router, prefix="/api/healthcheck", tags=["Healthcheck"])
