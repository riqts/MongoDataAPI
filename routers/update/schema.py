from typing import Dict, Any, Optional
from pydantic import BaseModel

from routers.schema import MongoRequestBaseSchema


class UpdateOneRequestBody(MongoRequestBaseSchema):
    filter: Dict[str, Any]
    update: Dict[str, Any]
    upsert: bool = False


class UpdateOneResponseBody(BaseModel):
    matched_count: int
    modified_count: int
    upserted_id: Optional[str] = None


class UpdateManyRequestBody(MongoRequestBaseSchema):
    filter: Dict[str, Any]
    update: Dict[str, Any]
    upsert: bool = False


class UpdateManyResponseBody(BaseModel):
    matched_count: int
    modified_count: int
    upsertedId: Optional[str] = None
