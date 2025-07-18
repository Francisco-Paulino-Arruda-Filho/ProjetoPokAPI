from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId

from models.PyObjectId import PyObjectId

class Pokemon(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: str
    height: str
    weight: str
    types: List[str]
    image: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}