from typing import Dict, Any
from pydantic import BaseModel

from routers.schema import MongoRequestBaseSchema


class DeleteOneRequestBody(MongoRequestBaseSchema):
    filter: Dict[str, Any]


class DeleteOneResponseBody(BaseModel):
    deleted_count: int


class DeleteManyRequestBody(MongoRequestBaseSchema):
    filter: Dict[str, Any]


class DeleteManyResponseBody(BaseModel):
    deleted_count: int