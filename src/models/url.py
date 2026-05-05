from pydantic import BaseModel, Field, ConfigDict, BeforeValidator, PlainSerializer
from typing import Optional, Annotated
from bson import ObjectId

# Custom type to handle MongoDB ObjectId serialization and validation for Pydantic models
PyObjectId = Annotated[
    str,
    BeforeValidator(lambda x: str(x) if isinstance(x, ObjectId) else x),
    PlainSerializer(lambda x: str(x), return_type=str)
]

class UrlInfo(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    url: str
    hostname: str
    path: str
    is_malicious: bool = False
    metadata: Optional[dict] = None

    model_config = ConfigDict(
        populate_by_name=True, # Allow using field names instead of aliases when creating instances
        arbitrary_types_allowed=True # Allow arbitrary types like ObjectId
    )