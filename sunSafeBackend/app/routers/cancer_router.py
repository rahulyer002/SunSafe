from fastapi import APIRouter
from app.services.cancer_service import get_cancer_incidence

router = APIRouter(prefix="/cancer", tags=["Cancer"])


@router.get("/")
def list_cancer():

    return get_cancer_incidence()