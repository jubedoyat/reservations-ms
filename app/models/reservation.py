from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class Luggage(BaseModel):
    hold_bags: int
    hand_bags: int


class Pet(BaseModel):
    species: str
    hold: bool


class ReservationBase(BaseModel):
    user_id: str
    flight_id: str
    seat: str
    boarding_time: datetime
    luggage: Optional[Luggage] = None
    pets: Optional[List[Pet]] = []


class ReservationCreate(BaseModel):
    flight_id: str
    seat: str
    boarding_time: datetime
    luggage: Optional[Luggage] = None
    pets: Optional[List[Pet]] = []


class ReservationUpdate(BaseModel):
    seat: Optional[str]
    boarding_time: Optional[datetime]
    luggage: Optional[Luggage]
    pets: Optional[List[Pet]]


class ReservationInDB(ReservationBase):
    id: str = Field(..., alias="_id")
    user_id: str

    class Config:
        validate_by_name = True
        from_attributes = True


class ReservationPublic(ReservationBase):
    id: str
