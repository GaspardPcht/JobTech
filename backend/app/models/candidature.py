from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.database import Base

class CandidatureStatus(enum.Enum):
    """
    Énumération des statuts possibles pour une candidature
    """
    PENDING = "pending"         # En attente
    APPLIED = "applied"         # Candidature envoyée
    INTERVIEW = "interview"     # Entretien prévu
    TECHNICAL_TEST = "technical_test"  # Test technique
    OFFER_RECEIVED = "offer_received"  # Offre reçue
    ACCEPTED = "accepted"       # Offre acceptée
    REJECTED = "rejected"       # Candidature rejetée
    WITHDRAWN = "withdrawn"     # Candidature retirée

class Candidature(Base):
    """
    Modèle représentant une candidature à une offre d'emploi
    """
    __tablename__ = "candidatures"

    id = Column(Integer, primary_key=True, index=True)
    offer_id = Column(Integer, ForeignKey("offers.id"), nullable=False)
    status = Column(Enum(CandidatureStatus), default=CandidatureStatus.PENDING)
    application_date = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    next_step = Column(String(255), nullable=True)  # Prochain rendez-vous ou action
    next_step_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations
    offer = relationship("Offer", back_populates="candidatures")
