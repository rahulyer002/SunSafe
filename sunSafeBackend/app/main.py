from fastapi import FastAPI

from app.routers.uv_router import router as uv_router
from app.routers.skin_router import router as skin_router
from app.routers.cancer_router import router as cancer_router

app = FastAPI(
    title="SunSafe API",
    version="1.0"
)

app.include_router(uv_router)
app.include_router(skin_router)
app.include_router(cancer_router)