from __future__ import annotations

import os
from functools import lru_cache
from typing import Any

from bson import ObjectId
from pymongo import MongoClient, DESCENDING


@lru_cache(maxsize=1)
def get_collection():
    mongo_uri = os.getenv("MONGODB_URI")
    database_name = os.getenv("DATABASE_NAME", "webguard")
    if not mongo_uri:
        return None
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    return client[database_name]["scans"]


async def save_scan(document: dict[str, Any]) -> str:
    collection = get_collection()
    if collection is None:
        return "local"
    result = collection.insert_one(document)
    return str(result.inserted_id)


async def fetch_history(limit: int = 20) -> list[dict[str, Any]]:
    collection = get_collection()
    if collection is None:
        return []
    records = collection.find().sort("timestamp", DESCENDING).limit(limit)
    return [_serialize(record) for record in records]


async def fetch_scan_by_id(scan_id: str) -> dict[str, Any] | None:
    collection = get_collection()
    if collection is None:
        return None
    try:
        record = collection.find_one({"_id": ObjectId(scan_id)})
        return _serialize(record) if record else None
    except Exception:
        return collection.find_one({"_id": scan_id})


def _serialize(record: dict[str, Any] | None) -> dict[str, Any]:
    if not record:
        return {}
    serialized = dict(record)
    serialized["scan_id"] = str(serialized.pop("_id"))
    return serialized
