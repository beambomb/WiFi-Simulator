from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)

class UserResponse(BaseModel):
    id: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class TokenData(BaseModel):
    user_id: str | None = None

class SimulationBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    room_width: float = Field(10.0, gt=0, le=100)
    room_length: float = Field(8.0, gt=0, le=100)
    room_height: float = Field(2.8, gt=0, le=20)
    grid_step: float = Field(0.25, gt=0.05, le=2.0)

class SimulationCreate(SimulationBase):
    agents_data: str | None = '{"routers":[],"walls":[],"devices":[]}'

class SimulationUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=100)
    room_width: float | None = Field(None, gt=0, le=100)
    room_length: float | None = Field(None, gt=0, le=100)
    room_height: float | None = Field(None, gt=0, le=20)
    grid_step: float | None = Field(None, gt=0.05, le=2.0)
    agents_data: str | None = None

class SimulationListItem(BaseModel):
    id: str
    title: str
    room_width: float
    room_length: float
    room_height: float
    updated_at: datetime

    class Config:
        from_attributes = True

class SimulationResponse(SimulationBase):
    id: str
    user_id: str
    agents_data: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
