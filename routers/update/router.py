from typing import List

from fastapi import APIRouter, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

import db

from routers.update.schema import UpdateOneRequestBody, UpdateOneResponseBody, UpdateManyRequestBody, UpdateManyResponseBody

updateRouter = APIRouter(
    tags=['update'],
)


@updateRouter.put("/updateOne", response_model=UpdateOneResponseBody)
async def update_one(request: UpdateOneRequestBody):
    """
    Update a single document in a collection.

    - **dataSource**: The name of a linked MongoDB Atlas data source.
    - **database**: The name of a database in the specified data source.
    - **collection**: The name of a collection in the specified database.
    - **filter**: A MongoDB query filter that matches documents.
    - **update**: The update operations to be applied to the matched document.

    Returns the number of documents matched and modified.
    """
    collection = db[request.collection]
    result = await collection.update_one(request.filter, request.update)
    if result.matched_count:
        return {"matched_count": result.matched_count, "modified_count": result.modified_count}
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Update failed")


@updateRouter.put("/updateMany", response_model=UpdateManyResponseBody)
async def update_many(request: UpdateManyRequestBody):
    """
    Update multiple documents in a collection.

    - **dataSource**: The name of a linked MongoDB Atlas data source.
    - **database**: The name of a database in the specified data source.
    - **collection**: The name of a collection in the specified database.
    - **filter**: A MongoDB query filter that matches documents.
    - **update**: The update operations to be applied to the matched documents.

    Returns the number of documents matched and modified.
    """
    collection = db[request.collection]
    result = await collection.update_many(request.filter, request.update)
    if result.matched_count:
        return {"matched_count": result.matched_count, "modified_count": result.modified_count}
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Update failed")