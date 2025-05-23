from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TechBase(BaseModel):
    """Schéma de base pour une technologie"""
    id: Optional[int] = None
    name: str
    category: Optional[str] = None
    description: Optional[str] = None

class TechCreate(TechBase):
    """Schéma pour la création d'une technologie"""
    pass

class TechUpdate(BaseModel):
    """Schéma pour la mise à jour d'une technologie"""
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None

class TechInDB(TechBase):
    """Schéma pour une technologie en base de données"""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        orm_mode = True  # Pour la compatibilité avec les anciennes versions

class TechWithStats(TechInDB):
    """Schéma pour une technologie avec des statistiques"""
    offer_count: int = 0
    
    class Config:
        from_attributes = True
        orm_mode = True  # Pour la compatibilité avec les anciennes versions
    
class TechTrend(BaseModel):
    """Schéma pour les tendances des technologies"""
    name: str
    category: Optional[str] = None
    count: int
    percentage: float
    
    class Config:
        from_attributes = True
        orm_mode = True  # Pour la compatibilité avec les anciennes versions
