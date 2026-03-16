from fastapi import APIRouter
from app.services.skin_service import get_skin_profiles

router = APIRouter(prefix="/skin", tags=["Skin"])


@router.get("/")
def list_skin():

    return get_skin_profiles()