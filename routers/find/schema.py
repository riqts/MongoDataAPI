from typing import Optional, Dict, Any

from pydantic import BaseModel

from routers.schema import MongoRequestBaseSchema


class FindOneRequestBody(MongoRequestBaseSchema):
    filter: Dict[str, Any]
    projection: Optional[Dict[str, int]] = None

class FindOneResponseBody(BaseModel):
    document: Optional[Dict[str, Any]] = None

class FindManyRequestBody(FindOneRequestBody):
    sort: Optional[Dict[str, int]] = None
    limit: Optional[int] = None
    skip: Optional[int] = None