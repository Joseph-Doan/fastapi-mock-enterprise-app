from fastapi import FastAPI
from app.api import login, devices

app = FastAPI(
    title="FastAPI Mock Enterprise App",
    docs_url="/docs",
    redoc_url=None,
    openapi_url="/openapi.json",
)

# Include routers
app.include_router(login.router)
app.include_router(devices.router)
