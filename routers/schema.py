from pydantic import BaseModel

class MongoRequestBaseSchema(BaseModel):
    data_source: str
    database: str
    collection: str