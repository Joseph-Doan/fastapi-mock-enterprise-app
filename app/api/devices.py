from fastapi import APIRouter, Depends
from app.api.auth import verify_token
from app.models.device import Device

router = APIRouter()

fake_devices = [
    Device(id=1, name="Smart Sensor", status="online"),
    Device(id=2, name="Edge Gateway", status="offline"),
]

@router.get("/devices", dependencies=[Depends(verify_token)])
def list_devices():
    return fake_devices
