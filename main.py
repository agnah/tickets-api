from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import Settings
from app.endpoints.area import router as area_router
from app.endpoints.healthcheck import router as healthcheck_router
from app.endpoints.ticket import router as tickets_router
from app.endpoints.usuario import router as usuario_router

app = FastAPI()
setings = Settings()

origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(healthcheck_router, prefix="/api/healthcheck", tags=["Healthcheck"])
app.include_router(tickets_router, prefix="/api/tickets", tags=["Tickets"])
app.include_router(area_router, prefix="/api/area", tags=["Area"])
app.include_router(usuario_router, prefix="/api/usuario", tags=["Usuario"])
