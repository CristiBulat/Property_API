from typing import List, Optional
from pydantic import BaseModel, Field


# Room Schemas
class RoomBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Room name")
    area: float = Field(..., gt=0, description="Room area in square meters")


class Room(RoomBase):
    id: int = Field(..., description="Unique ID of the room")
    property_id: int = Field(..., description="Associated property ID")

    class Config:
        from_attributes = True


class RoomCreate(RoomBase):
    pass


class RoomUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Updated name of the room")
    area: Optional[float] = Field(None, gt=0, description="Updated area of the room")


# Property Schemas
class PropertyBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, description="Property title")
    description: str = Field(..., max_length=500, description="Detailed description")
    price: float = Field(..., gt=0, description="Price of the property in USD")
    address: str = Field(..., min_length=5, description="Full address of the property")


class Property(PropertyBase):
    id: int = Field(..., description="Unique ID of the property")
    rooms: Optional[List[Room]] = Field(None, description="List of rooms in the property")

    class Config:
        from_attributes = True


class PropertyCreate(PropertyBase):
    pass


class PropertyUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100, description="Updated title")
    description: Optional[str] = Field(None, max_length=500, description="Updated description")
    price: Optional[float] = Field(None, gt=0, description="Updated price")
    address: Optional[str] = Field(None, min_length=5, description="Updated address")


# Pagination Schema
class PaginatedProperties(BaseModel):
    items: List[Property] = Field(..., description="List of properties on the current page")
    total: int = Field(..., ge=0, description="Total number of properties")
    page: int = Field(..., ge=1, description="Current page number")
    size: int = Field(..., ge=1, description="Number of items per page")
