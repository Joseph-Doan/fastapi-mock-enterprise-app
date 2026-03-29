import time
import uuid
import logging

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from app.api import auth, devices
from app.ui import router as ui_router
from app.core.logging_config import setup_logging

app = FastAPI(
    title="FastAPI Mock Enterprise App",
    docs_url="/docs",
    redoc_url=None,
    openapi_url="/openapi.json",
)

setup_logging()
logger = logging.getLogger(__name__)

app.include_router(auth.router, prefix="/api")
app.include_router(devices.router, prefix="/api")
app.include_router(ui_router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}

@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    request.state.request_id = request_id

    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    logger.info({
        "request_id": request_id,
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
        "process_time": process_time,
    })

    response.headers["X-Request-ID"] = request_id
    return response