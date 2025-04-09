from fastapi import APIRouter, HTTPException, Depends, Request, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List

from app.core.security import get_current_user_id
from app.db.mongodb import get_database
from app.db.repositories.reservation_repo import ReservationRepository
from app.models.reservation import ReservationCreate, ReservationUpdate, ReservationPublic
import httpx

router = APIRouter(prefix="/reservations", tags=["Reservations"])


async def validate_external_ids(user_id: str, flight_id: str):
    async with httpx.AsyncClient() as client:
        user_res = await client.get(f"http://localhost:8000/users/{user_id}")
        flight_res = await client.get(f"http://localhost:8001/flights/{flight_id}")
        if user_res.status_code != 200:
            raise HTTPException(status_code=400, detail="User not found")
        if flight_res.status_code != 200:
            raise HTTPException(status_code=400, detail="Flight not found")

@router.get("/", response_model=List[ReservationPublic])
async def list_reservations(db: AsyncIOMotorDatabase = Depends(get_database)):
    repo = ReservationRepository(db)
    reservations = await repo.list()
    return [ReservationPublic(**r.model_dump()) for r in reservations]

@router.get("/auth-debug")
async def auth_debug(user_id: str = Depends(get_current_user_id)):
    return {"user_id": user_id}

@router.get("/{reservation_id}", response_model=ReservationPublic)
async def get_reservation(reservation_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    repo = ReservationRepository(db)
    reservation = await repo.get_by_id(reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return ReservationPublic(**reservation.model_dump())


@router.patch("/{reservation_id}", response_model=ReservationPublic)
async def update_reservation(
    reservation_id: str,
    update: ReservationUpdate,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    repo = ReservationRepository(db)
    updated = await repo.update(reservation_id, update)
    if not updated:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return ReservationPublic(**updated.model_dump())


@router.post("/", response_model=ReservationPublic, status_code=status.HTTP_201_CREATED)
async def create_reservation(
    reservation_data: ReservationCreate,
    db: AsyncIOMotorDatabase = Depends(get_database),
    user_id: str = Depends(get_current_user_id)
):
    reservation = reservation_data.model_dump()
    reservation["user_id"] = user_id

    await validate_external_ids(user_id, reservation["flight_id"])

    repo = ReservationRepository(db)
    created = await repo.create(reservation)
    return ReservationPublic(**created.model_dump())


@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reservation(
    reservation_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    user_id: str = Depends(get_current_user_id)
):
    repo = ReservationRepository(db)
    reservation = await repo.get_by_id(reservation_id)

    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    if reservation.user_id != user_id:
        raise HTTPException(status_code=403, detail="You are not allowed to delete this reservation")

    deleted = await repo.delete(reservation_id)
    if not deleted:
        raise HTTPException(status_code=500, detail="Failed to delete reservation")
