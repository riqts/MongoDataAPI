from typing import List

from fastapi import APIRouter, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

import db

from routers.aggregate.schema import AggregateRequestBody

aggregateRouter = APIRouter(
    tags=['aggregate'],
    prefix='/blog'
)


@aggregateRouter.post("/aggregate", response_model=List[dict])
async def aggregate(request: AggregateRequestBody):
    """
    Aggregate documents in a collection.

    - **dataSource**: The name of a linked MongoDB Atlas data source.
    - **database**: The name of a database in the specified data source.
    - **collection**: The name of a collection in the specified database.
    - **pipeline**: The aggregation pipeline to apply.

    Returns the aggregated documents.
    """
    collection = db[request.collection]
    cursor = collection.aggregate(request.pipeline)
    results = await cursor.to_list(length=None)
    if results:
        return results
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Aggregation failed")