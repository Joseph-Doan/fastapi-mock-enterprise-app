from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api import login, devices
from app.ui import router as ui_router

app = FastAPI(
    title="FastAPI Mock Enterprise App",
    docs_url="/docs",
    redoc_url=None,
    openapi_url="/openapi.json",
)

# Include routers
app.include_router(login.router, prefix="/api")
app.include_router(devices.router, prefix="/api")

app.include_router(ui_router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
