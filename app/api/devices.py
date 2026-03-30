from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from app.api.auth import verify_token

router = APIRouter()

class Device(BaseModel):
    id: int
    name: str
    status: str

class DeviceCreate(BaseModel):
    name: str
    status: str

class DeviceUpdate(BaseModel):
    name: str | None = None
    status: str | None = None

DEVICES = [
    {"id": 1, "name": "Router-01", "status": "online"},
    {"id": 2, "name": "Switch-01", "status": "offline"},
]

@router.get("/devices", response_model=list[Device], tags=["Devices"])
def get_devices(_: str = Depends(verify_token)):
    return DEVICES

@router.post("/devices", response_model=Device, status_code=status.HTTP_201_CREATED, tags=["Devices"])
def create_device(payload: DeviceCreate, _: str = Depends(verify_token)):
    new_id = max([d["id"] for d in DEVICES], default=0) + 1
    device = {"id": new_id, "name": payload.name, "status": payload.status}
    DEVICES.append(device)
    return device

@router.get("/devices/{device_id}", response_model=Device, tags=["Devices"])
def get_device(device_id: int, _: str = Depends(verify_token)):
    for d in DEVICES:
        if d["id"] == device_id:
            return d
    raise HTTPException(status_code=404, detail="Device not found")

@router.put("/devices/{device_id}", response_model=Device, tags=["Devices"])
def update_device(device_id: int, payload: DeviceUpdate, _: str = Depends(verify_token)):
    for d in DEVICES:
        if d["id"] == device_id:
            if payload.name is not None:
                d["name"] = payload.name
            if payload.status is not None:
                d["status"] = payload.status
            return d
    raise HTTPException(status_code=404, detail="Device not found")

@router.delete("/devices/{device_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Devices"])
def delete_device(device_id: int, _: str = Depends(verify_token)):
    for i, d in enumerate(DEVICES):
        if d["id"] == device_id:
            DEVICES.pop(i)
            return
    raise HTTPException(status_code=404, detail="Device not found")