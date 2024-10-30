import logging
from typing import Union

from contextlib import asynccontextmanager
from devtools import debug
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from mongo_client import MongoDBClient

import config

from routers.aggregate.router import aggregateRouter
from routers.delete.router import deleteRouter
from routers.find.router import findRouter
from routers.insert.router import insertRouter
from routers.update.router import updateRouter

logger = logging.getLogger(__name__)

app = FastAPI()


MONGODB_URI = config.MONGODB_URI


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("successfully started")
    MongoDBClient.get_instance()
    yield
    MongoDBClient.get_instance().close()


app = FastAPI(lifespan=lifespan, docs_url='/api/docs', openapi_url='/openapi.json', )
client = None

app.swagger_ui_parameters = {
    "docExpansion": "none",
    "filter": True,
}

origins = ["http://localhost:3000",
           "https://sponsorpad.co",
           "https://staging.sponsorpad.co",
           "https://www.sponsorpad.co",
           "https://admin.sponsorpad.co",
           config.FRONTEND_URL]

if config.ENVIRONMENT == "local":
    origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(findRouter)
app.include_router(updateRouter)
app.include_router(insertRouter)
app.include_router(deleteRouter)
app.include_router(aggregateRouter)


async def http422_error_handler(
        _: Request, exc: Union[RequestValidationError, ValidationError]
) -> JSONResponse:
    debug(exc.errors())
    return JSONResponse(
        {"errors": exc.errors()}, status_code=HTTP_422_UNPROCESSABLE_ENTITY
    )


app.add_exception_handler(ValidationError, http422_error_handler)
app.add_exception_handler(RequestValidationError, http422_error_handler)
