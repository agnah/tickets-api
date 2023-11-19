from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.logger import logger

from app.dependencies.db import get_db
from app.models import SessionLocal

router = APIRouter()


class UnhealthyException(Exception):
    pass

@router.get("/")
async def healthcheck():
    return {"status": "HEALTHY"}

