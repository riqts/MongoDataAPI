from typing import List, Dict, Any

from routers.schema import MongoRequestBaseSchema


class AggregateRequestBody(MongoRequestBaseSchema):
    pipeline: List[Dict[str, Any]]
