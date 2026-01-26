from fastapi import FastAPI
from app.api import auth, devices

app = FastAPI(title="SDET Mock Enterprise API")

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(auth.router, prefix="/api")
app.include_router(devices.router, prefix="/api")
