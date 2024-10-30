from fastapi import APIRouter, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

import db

from routers.delete.schema import DeleteOneRequestBody, DeleteOneResponseBody, DeleteManyRequestBody, DeleteManyResponseBody

deleteRouter = APIRouter(
    tags=['delete'],
)


@deleteRouter.delete("/deleteOne", response_model=DeleteOneResponseBody)
async def delete_one(request: DeleteOneRequestBody):
    """
    Delete a single document from a collection.

    - **dataSource**: The name of a linked MongoDB Atlas data source.
    - **database**: The name of a database in the specified data source.
    - **collection**: The name of a collection in the specified database.
    - **filter**: A MongoDB query filter that matches documents.

    Returns the number of documents deleted.
    """
    collection = db[request.collection]
    result = await collection.delete_one(request.filter)
    if result.deleted_count:
        return {"deleted_count": result.deleted_count}
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Delete failed")


@deleteRouter.delete("/deleteMany", response_model=DeleteManyResponseBody)
async def delete_many(request: DeleteManyRequestBody):
    """
    Delete multiple documents from a collection.

    - **dataSource**: The name of a linked MongoDB Atlas data source.
    - **database**: The name of a database in the specified data source.
    - **collection**: The name of a collection in the specified database.
    - **filter**: A MongoDB query filter that matches documents.

    Returns the number of documents deleted.
    """
    collection = db[request.collection]
    result = await collection.delete_many(request.filter)
    if result.deleted_count:
        return {"deleted_count": result.deleted_count}
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Delete failed")