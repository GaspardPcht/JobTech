from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class CandidatureStatus(str, Enum):
    """Énumération des statuts possibles pour une candidature"""
    PENDING = "pending"
    APPLIED = "applied"
    INTERVIEW = "interview"
    TECHNICAL_TEST = "technical_test"
    OFFER_RECEIVED = "offer_received"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"

class CandidatureBase(BaseModel):
    """Schéma de base pour une candidature"""
    offer_id: int
    status: CandidatureStatus = CandidatureStatus.PENDING
    application_date: Optional[datetime] = None
    notes: Optional[str] = None
    next_step: Optional[str] = None
    next_step_date: Optional[datetime] = None

class CandidatureCreate(CandidatureBase):
    """Schéma pour la création d'une candidature"""
    pass

class CandidatureUpdate(BaseModel):
    """Schéma pour la mise à jour d'une candidature"""
    status: Optional[CandidatureStatus] = None
    application_date: Optional[datetime] = None
    notes: Optional[str] = None
    next_step: Optional[str] = None
    next_step_date: Optional[datetime] = None

class CandidatureInDB(CandidatureBase):
    """Schéma pour une candidature en base de données"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class OfferBasicInfo(BaseModel):
    """Informations de base sur une offre pour l'inclusion dans une candidature"""
    id: int
    title: str
    company: str
    location: Optional[str] = None
    contract_type: Optional[str] = None
    
    class Config:
        from_attributes = True

class CandidatureResponse(CandidatureInDB):
    """Schéma pour la réponse d'une candidature avec les informations de l'offre"""
    offer: Optional[OfferBasicInfo] = None
