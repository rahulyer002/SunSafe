from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.uv_router import router as uv_router
from app.routers.skin_router import router as skin_router
from app.routers.cancer_router import router as cancer_router

app = FastAPI(
    title="SunSafe API",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(uv_router)
app.include_router(skin_router)
app.include_router(cancer_router)

@app.get("/")
def root():
    return {"message": "SunSafe API running"}
