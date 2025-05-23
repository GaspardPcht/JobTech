from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base

# Table d'association entre offres et technologies
offer_tech = Table(
    'offer_tech',
    Base.metadata,
    Column('offer_id', Integer, ForeignKey('offers.id'), primary_key=True),
    Column('tech_id', Integer, ForeignKey('techs.id'), primary_key=True)
)

class Offer(Base):
    """
    Modèle représentant une offre d'emploi
    """
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    location = Column(String(255))
    description = Column(Text)
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    contract_type = Column(String(50))  # CDI, CDD, Freelance, Stage, etc.
    remote = Column(Boolean, default=False)
    url = Column(String(512))
    posted_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations
    techs = relationship("Tech", secondary=offer_tech, back_populates="offers")
    candidatures = relationship("Candidature", back_populates="offer")
