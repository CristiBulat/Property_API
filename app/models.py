from sqlalchemy import Boolean, Integer, String, Float, Column, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base, SessionLocal, engine


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    address = Column(String, nullable=False)

    # Relationship with Room
    rooms = relationship("Room", back_populates="property", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Property(id={self.id}, title={self.title}, price={self.price}, address={self.address})>"


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    area = Column(Float, nullable=False)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)

    property = relationship("Property", back_populates="rooms")

    def __repr__(self):
        return f"<Room(id={self.id}, name={self.name}, area={self.area}, property_id={self.property_id})>"

