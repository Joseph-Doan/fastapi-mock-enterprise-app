from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from pydantic import BaseModel
from app.core.security import get_current_user

router = APIRouter(prefix="/api", tags=["Devices"])

# ----- Models -----
class Device(BaseModel):
    id: int
    name: str
    status: str  # online/offline

class DeviceCreate(BaseModel):
    name: str
    status: str

class DeviceUpdate(BaseModel):
    name: str = None
    status: str = None

# ----- In-Memory Storage -----
mock_devices: List[Device] = [
    Device(id=1, name="Smart Sensor", status="online"),
    Device(id=2, name="Edge Gateway", status="offline"),
]

# ----- CRUD Endpoints -----

@router.get("/devices", response_model=List[Device])
def get_devices(user: str = Depends(get_current_user)):
    return mock_devices

@router.get("/devices/{device_id}", response_model=Device)
def get_device(device_id: int, user: str = Depends(get_current_user)):
    for device in mock_devices:
        if device.id == device_id:
            return device
    raise HTTPException(status_code=404, detail="Device not found")

@router.post("/devices", response_model=Device, status_code=status.HTTP_201_CREATED)
def create_device(device: DeviceCreate, user: str = Depends(get_current_user)):
    new_id = max([d.id for d in mock_devices], default=0) + 1
    new_device = Device(id=new_id, name=device.name, status=device.status)
    mock_devices.append(new_device)
    return new_device

@router.put("/devices/{device_id}", response_model=Device)
def update_device(device_id: int, device_update: DeviceUpdate, user: str = Depends(get_current_user)):
    for device in mock_devices:
        if device.id == device_id:
            if device_update.name is not None:
                device.name = device_update.name
            if device_update.status is not None:
                device.status = device_update.status
            return device
    raise HTTPException(status_code=404, detail="Device not found")

@router.delete("/devices/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device(device_id: int, user: str = Depends(get_current_user)):
    for i, device in enumerate(mock_devices):
        if device.id == device_id:
            mock_devices.pop(i)
            return
    raise HTTPException(status_code=404, detail="Device not found")
