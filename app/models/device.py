from pydantic import BaseModel

class Device(BaseModel):
    id: int
    name: str
    status: str