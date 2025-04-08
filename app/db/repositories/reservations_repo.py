from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Optional
from bson import ObjectId
from app.models.reservation import ReservationCreate, ReservationUpdate, ReservationInDB


def normalize_mongo_id(doc: dict) -> dict:
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc


class ReservationRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["Reservations"]

    async def get_by_id(self, reservation_id: str) -> Optional[ReservationInDB]:
        if not ObjectId.is_valid(reservation_id):
            return None
        doc = await self.collection.find_one({"_id": ObjectId(reservation_id)})
        return ReservationInDB(**normalize_mongo_id(doc)) if doc else None

    async def list(self) -> List[ReservationInDB]:
        reservations = []
        async for doc in self.collection.find():
            reservations.append(ReservationInDB(**normalize_mongo_id(doc)))
        return reservations

    async def create(self, reservation: ReservationCreate) -> ReservationInDB:
        doc = reservation.model_dump()
        result = await self.collection.insert_one(doc)
        doc["_id"] = str(result.inserted_id)
        return ReservationInDB(**doc)

    async def update(self, reservation_id: str, update_data: ReservationUpdate) -> Optional[ReservationInDB]:
        if not ObjectId.is_valid(reservation_id):
            return None
        update = {k: v for k, v in update_data.model_dump().items() if v is not None}
        await self.collection.update_one({"_id": ObjectId(reservation_id)}, {"$set": update})
        return await self.get_by_id(reservation_id)

    async def delete(self, reservation_id: str) -> bool:
        if not ObjectId.is_valid(reservation_id):
            return False
        result = await self.collection.delete_one({"_id": ObjectId(reservation_id)})
        return result.deleted_count == 1
