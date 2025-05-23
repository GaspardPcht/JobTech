from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional
from datetime import datetime

class TechBase(BaseModel):
    """Schéma de base pour une technologie"""
    id: int
    name: str

class OfferBase(BaseModel):
    """Schéma de base pour une offre d'emploi"""
    title: str
    company: str
    location: Optional[str] = None
    description: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    contract_type: Optional[str] = None
    remote: bool = False
    url: Optional[str] = None

class OfferCreate(OfferBase):
    """Schéma pour la création d'une offre d'emploi"""
    tech_ids: Optional[List[int]] = []

class OfferUpdate(BaseModel):
    """Schéma pour la mise à jour d'une offre d'emploi"""
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    contract_type: Optional[str] = None
    remote: Optional[bool] = None
    url: Optional[str] = None
    tech_ids: Optional[List[int]] = None

class OfferInDB(OfferBase):
    """Schéma pour une offre d'emploi en base de données"""
    id: int
    posted_at: datetime
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        orm_mode = True  # Pour la compatibilité avec les anciennes versions

class OfferResponse(OfferInDB):
    """Schéma pour la réponse d'une offre d'emploi avec ses technologies"""
    techs: List[TechBase] = []
    
    class Config:
        from_attributes = True
        orm_mode = True  # Pour la compatibilité avec les anciennes versions
