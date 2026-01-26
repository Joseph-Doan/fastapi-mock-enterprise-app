from fastapi import APIRouter, Header, HTTPException
from app.models.auth import LoginRequest

router = APIRouter()

FAKE_TOKEN = "fake-jwt-token"

@router.post("/login")
def login(payload: LoginRequest):
    if payload.username == "admin" and payload.password == "password":
        return {
            "access_token": FAKE_TOKEN,
            "token_type": "bearer"
        }
    raise HTTPException(status_code=401, detail="Invalid credentials")


def verify_token(authorization: str = Header(None)):
    if authorization != f"Bearer {FAKE_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")
