from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId
from models.PyObjectId import PyObjectId

class Pokemon(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")  # pega o _id do Mongo
    number: int  # número da Pokédex
    name: str
    description: str
    height: str
    weight: str
    types: List[str]
    image: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        extra = "ignore"
        json_encoders = {ObjectId: str}
