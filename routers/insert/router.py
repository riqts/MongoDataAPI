from typing import List

from fastapi import APIRouter, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

import db

from routers.insert.schema import InsertOneRequestBody, InsertOneResponseBody, InsertManyRequestBody, InsertManyResponseBody

insertRouter = APIRouter(
    tags=['insert'],
)


@insertRouter.post("/insertOne", response_model=InsertOneResponseBody)
async def insert_one(request: InsertOneRequestBody):
    """
    Insert a single document into a collection.

    - **dataSource**: The name of a linked MongoDB Atlas data source.
    - **database**: The name of a database in the specified data source.
    - **collection**: The name of a collection in the specified database.
    - **document**: The document to insert.

    Returns the inserted document's ID.
    """
    collection = db[request.collection]
    result = await collection.insert_one(request.document)
    if result.inserted_id:
        return {"inserted_id": str(result.inserted_id)}
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Insert failed")


@insertRouter.post("/insertMany", response_model=InsertManyResponseBody)
async def insert_many(request: InsertManyRequestBody):
    """
    Insert multiple documents into a collection.

    - **dataSource**: The name of a linked MongoDB Atlas data source.
    - **database**: The name of a database in the specified data source.
    - **collection**: The name of a collection in the specified database.
    - **documents**: The documents to insert.

    Returns the inserted documents' IDs.
    """
    collection = db[request.collection]
    result = await collection.insert_many(request.documents)
    if result.inserted_ids:
        return {"inserted_ids": [str(id) for id in result.inserted_ids]}
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Insert failed")