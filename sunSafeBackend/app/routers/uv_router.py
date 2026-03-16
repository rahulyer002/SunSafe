from fastapi import APIRouter
from app.services.uv_service import get_uv_trend

router = APIRouter(prefix="/uv", tags=["UV"])


@router.get("/")
def list_uv():

    return get_uv_trend()