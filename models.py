from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional

# Getting Started with MongoDB and FastAPI | MongoDB - https://tmpl.at/3RR1j2v


class PyObjectId(ObjectId):
    '''
    Helper class to convert ObjectId to string and vice versa
    '''
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Book(BaseModel):
    '''
    Book model
    '''
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    isbn: str = Field(...)
    title: str = Field(...)
    author: Optional[str] = Field(None)
    price: float = Field(..., ge=0)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "isbn": "111-111-1111",
                "title": "Flask for cool people!",
                "price": 9.99
            }
        }
