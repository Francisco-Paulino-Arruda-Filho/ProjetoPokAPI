from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId

from models.PyObjectId import PyObjectId
from models.Pokemon import Pokemon

class Team(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    team: List[Optional[Pokemon]] = Field(default_factory=lambda: [None] * 6)
    user_id: PyObjectId = Field(default_factory=PyObjectId, alias="user_id")

    class Config:
        validate_by_name = True  
        extra = "ignore"
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
