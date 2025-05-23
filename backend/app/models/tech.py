from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base
from app.models.offer import offer_tech

class Tech(Base):
    """
    Modèle représentant une technologie ou compétence
    """
    __tablename__ = "techs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    category = Column(String(50))  # Frontend, Backend, Database, DevOps, etc.
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations
    offers = relationship("Offer", secondary=offer_tech, back_populates="techs")
