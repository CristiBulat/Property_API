from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)


app = FastAPI(title="Property API")


# Dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Property CRUD Operations
@app.post('/properties', response_model=schemas.Property)
async def create_property(
    property: schemas.PropertyCreate,
    db: Session = Depends(get_db)
):
    db_property = models.Property(**property.dict())
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property

@app.get('/properties', response_model=schemas.PaginatedProperties)
async def list_properties(
    page: int = Query(1, gt=0),
    size: int = Query(10, gt=0),
    db: Session = Depends(get_db)
):
    skip = (page - 1) * size
    total = db.query(models.Property).count()
    properties = db.query(models.Property).offset(skip).limit(size).all()

    return{
        "items": properties,
        "total": total,
        "page": page,
        "size": size
    }


@app.get('/properties/{property_id}', response_model=schemas.Property)
async def get_property(
        property_id: int,
        db: Session = Depends(get_db)
):
    property = db.query(models.Property).filter(models.Property.id == property_id).first()
    if property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return property


@app.put('/properties/{property_id}', response_model=schemas.Property)
async def update_property(
        property_id: int,
        property: schemas.PropertyUpdate,
        db: Session = Depends(get_db),
):
    db_property = db.query(models.Property).filter(models.Property.id == property_id).first()
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")

    for key, value in property.dict(exclude_unset=True).items():
        setattr(db_property, key, value)

    db.commit()
    db.refresh(db_property)
    return db_property

@app.delete('/properties/{property_id}')
async def delete_property(
        property_id: int,
        db: Session = Depends(get_db),
):
    property = db.query(models.Property).filter(models.Property.id == property_id).first()
    if property is None:
        raise HTTPException(status_code=404, detail="Property not found")

    db.delete(property)
    db.commit()
    return {"message": "Property deleted successfully"}


# Room CRUD Operations

@app.post("/properties/{property_id}/rooms/", response_model=schemas.Room)
async def create_room(
        property_id: int,
        room: schemas.RoomCreate,
        db: Session = Depends(get_db),
):
    property = db.query(models.Property).filter(models.Property.id == property_id).first()
    if property is None:
        raise HTTPException(status_code=404, detail="Property not found")

    db_room = models.Room(**room.dict(), property_id=property_id)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


@app.get("/properties/{property_id}/rooms/", response_model=List[schemas.Room])
async def list_rooms(
        property_id: int,
        db: Session = Depends(get_db)
):
    property = db.query(models.Property).filter(models.Property.id == property_id).first()
    if property is None:
        raise HTTPException(status_code=404, detail="Property not found")

    rooms = db.query(models.Room).filter(models.Room.property_id == property_id).all()
    return rooms


@app.get("/properties/{property_id}/rooms/{room_id}", response_model=schemas.Room)
async def get_room(
        property_id: int,
        room_id: int,
        db: Session = Depends(get_db)
):
    room = db.query(models.Room).filter(
        models.Room.property_id == property_id,
        models.Room.id == room_id
    ).first()
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return room


@app.put("/properties/{property_id}/rooms/{room_id}", response_model=schemas.Room)
async def update_room(
        property_id: int,
        room_id: int,
        room: schemas.RoomUpdate,
        db: Session = Depends(get_db),
):
    db_room = db.query(models.Room).filter(
        models.Room.property_id == property_id,
        models.Room.id == room_id
    ).first()
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    for key, value in room.dict(exclude_unset=True).items():
        setattr(db_room, key, value)

    db.commit()
    db.refresh(db_room)
    return db_room


@app.delete("/properties/{property_id}/rooms/{room_id}")
async def delete_room(
        property_id: int,
        room_id: int,
        db: Session = Depends(get_db),
):
    room = db.query(models.Room).filter(
        models.Room.property_id == property_id,
        models.Room.id == room_id
    ).first()
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    db.delete(room)
    db.commit()
    return {"message": "Room deleted successfully"}
