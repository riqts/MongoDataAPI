from typing import List

from fastapi import APIRouter, Depends, status, Response, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase

import db

from routers.find.schema import FindOneResponseBody, FindOneRequestBody, FindManyRequestBody

findRouter = APIRouter(
    tags=['find'],
)


@findRouter.get("/findOne", response_model=FindOneResponseBody)
async def find_one(request: FindOneRequestBody):
    """
    Find a single document that matches a query.

    - **dataSource**: The name of a linked MongoDB Atlas data source.
    - **database**: The name of a database in the specified data source.
    - **collection**: The name of a collection in the specified database.
    - **filter**: A MongoDB query filter that matches documents.
    - **projection**: A MongoDB projection for matched documents returned by the operation.

    Returns a document that matches the specified filter. If no documents match, returns `null`.
    """
    collection = db[request.collection]
    document = collection.find_one(request.filter, request.projection)
    if document:
        return {"document": document}
    return None


@findRouter.get("/find", response_model=List[FindOneResponseBody])
async def find_many(request: FindManyRequestBody):
    """
    Find all documents that match a query.

    - **dataSource**: The name of a linked MongoDB Atlas data source.
    - **database**: The name of a database in the specified data source.
    - **collection**: The name of a collection in the specified database.
    - **filter**: A MongoDB query filter that matches documents.
    - **projection**: A MongoDB projection for matched documents returned by the operation.
    - **sort**: A MongoDB sort specification for matched documents returned by the operation.
    - **limit**: The maximum number of documents to return.
    - **skip**: The number of documents to skip before returning the first document.

    Returns an array of documents that match the specified filter. If no documents match, returns an empty array.
    """
    collection = db[request.collection]
    cursor = collection.find(request.filter, request.projection)

    if request.sort:
        cursor = cursor.sort(request.sort)
    if request.limit:
        cursor = cursor.limit(request.limit)
    if request.skip:
        cursor = cursor.skip(request.skip)

    documents = await cursor.to_list(length=request.limit or 100)
    return documents