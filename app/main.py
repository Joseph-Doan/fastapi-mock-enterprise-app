from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api import login, devices
from app.ui import router as ui_router

from app.core.logging_config import setup_logging
import logging

from fastapi import Request

app = FastAPI(
    title="FastAPI Mock Enterprise App",
    docs_url="/docs",
    redoc_url=None,
    openapi_url="/openapi.json",
)

setup_logging()
logger = logging.getLogger(__name__)

# Include routers
app.include_router(login.router, prefix="/api")
app.include_router(devices.router, prefix="/api")

app.include_router(ui_router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}

@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)

    logger.info(
        "Incoming request",
        extra={
            "path": request.url.path,
            "method": request.method,
        },
    )

    return response