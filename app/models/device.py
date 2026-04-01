from typing import Optional

from pydantic import BaseModel

class Device(BaseModel):
    id: int
    name: str
    status: str


class DeviceCreate(BaseModel):
    name: str
    status: str


class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None