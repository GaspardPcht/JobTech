from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from datetime import datetime

from app.database import get_db
from app.services.candidature_service import CandidatureService
from app.schemas.candidature import (
    CandidatureCreate, CandidatureUpdate, CandidatureResponse,
    CandidatureStatus
)

router = APIRouter(
    prefix="/candidatures",
    tags=["candidatures"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[CandidatureResponse])
async def read_candidatures(
    skip: int = 0,
    limit: int = 100,
    status: Optional[CandidatureStatus] = None,
    offer_id: Optional[int] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """
    Récupère une liste de candidatures avec pagination et filtres optionnels
    """
    filters = {}
    if status:
        filters["status"] = status
    if offer_id:
        filters["offer_id"] = offer_id
    if date_from:
        filters["date_from"] = date_from
    if date_to:
        filters["date_to"] = date_to
    
    candidatures = CandidatureService.get_candidatures(db, skip=skip, limit=limit, filters=filters)
    return candidatures

@router.get("/stats", response_model=Dict[str, int])
async def read_candidature_stats(db: Session = Depends(get_db)):
    """
    Récupère des statistiques sur les candidatures par statut
    """
    return CandidatureService.get_candidature_stats(db)

@router.get("/{candidature_id}", response_model=CandidatureResponse)
async def read_candidature(candidature_id: int, db: Session = Depends(get_db)):
    """
    Récupère une candidature spécifique par son ID
    """
    candidature = CandidatureService.get_candidature(db, candidature_id=candidature_id)
    if candidature is None:
        raise HTTPException(status_code=404, detail="Candidature non trouvée")
    return candidature

@router.post("/", response_model=CandidatureResponse, status_code=status.HTTP_201_CREATED)
async def create_candidature(candidature: CandidatureCreate, db: Session = Depends(get_db)):
    """
    Crée une nouvelle candidature
    """
    try:
        return CandidatureService.create_candidature(db=db, candidature=candidature)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{candidature_id}", response_model=CandidatureResponse)
async def update_candidature(
    candidature_id: int, 
    candidature: CandidatureUpdate, 
    db: Session = Depends(get_db)
):
    """
    Met à jour une candidature existante
    """
    updated_candidature = CandidatureService.update_candidature(
        db=db, 
        candidature_id=candidature_id, 
        candidature_data=candidature
    )
    if updated_candidature is None:
        raise HTTPException(status_code=404, detail="Candidature non trouvée")
    return updated_candidature

@router.delete("/{candidature_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_candidature(candidature_id: int, db: Session = Depends(get_db)):
    """
    Supprime une candidature
    """
    success = CandidatureService.delete_candidature(db=db, candidature_id=candidature_id)
    if not success:
        raise HTTPException(status_code=404, detail="Candidature non trouvée")
    return None
