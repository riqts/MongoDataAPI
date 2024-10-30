from typing import Dict, Any, List
from pydantic import BaseModel

from routers.schema import MongoRequestBaseSchema


class InsertOneRequestBody(MongoRequestBaseSchema):
    document: Dict[str, Any]


class InsertOneResponseBody(BaseModel):
    inserted_id: str


class InsertManyRequestBody(BaseModel):
    documents: List[Dict[str, Any]]


class InsertManyResponseBody(BaseModel):
    inserted_ids: List[str]