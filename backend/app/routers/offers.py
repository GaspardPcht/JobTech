from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.services.offer_service import OfferService
from app.schemas.offer import OfferCreate, OfferUpdate, OfferResponse

router = APIRouter(
    prefix="/offers",
    tags=["offers"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[OfferResponse])
async def read_offers(
    skip: int = 0,
    limit: int = 100,
    title: Optional[str] = None,
    company: Optional[str] = None,
    location: Optional[str] = None,
    contract_type: Optional[str] = None,
    remote: Optional[bool] = None,
    tech_ids: Optional[List[int]] = Query(None),
    min_salary: Optional[int] = None,
    max_salary: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Récupère une liste d'offres d'emploi avec pagination et filtres optionnels
    """
    filters = {}
    if title:
        filters["title"] = title
    if company:
        filters["company"] = company
    if location:
        filters["location"] = location
    if contract_type:
        filters["contract_type"] = contract_type
    if remote is not None:
        filters["remote"] = remote
    if tech_ids:
        filters["tech_ids"] = tech_ids
    if min_salary:
        filters["min_salary"] = min_salary
    if max_salary:
        filters["max_salary"] = max_salary
    
    offers = OfferService.get_offers(db, skip=skip, limit=limit, filters=filters)
    return offers

@router.get("/{offer_id}", response_model=OfferResponse)
async def read_offer(offer_id: int, db: Session = Depends(get_db)):
    """
    Récupère une offre d'emploi spécifique par son ID
    """
    offer = OfferService.get_offer(db, offer_id=offer_id)
    if offer is None:
        raise HTTPException(status_code=404, detail="Offre non trouvée")
    return offer

@router.post("/", response_model=OfferResponse, status_code=status.HTTP_201_CREATED)
async def create_offer(offer: OfferCreate, db: Session = Depends(get_db)):
    """
    Crée une nouvelle offre d'emploi
    """
    return OfferService.create_offer(db=db, offer=offer)

@router.put("/{offer_id}", response_model=OfferResponse)
async def update_offer(offer_id: int, offer: OfferUpdate, db: Session = Depends(get_db)):
    """
    Met à jour une offre d'emploi existante
    """
    updated_offer = OfferService.update_offer(db=db, offer_id=offer_id, offer_data=offer)
    if updated_offer is None:
        raise HTTPException(status_code=404, detail="Offre non trouvée")
    return updated_offer

@router.delete("/{offer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_offer(offer_id: int, db: Session = Depends(get_db)):
    """
    Supprime une offre d'emploi
    """
    success = OfferService.delete_offer(db=db, offer_id=offer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Offre non trouvée")
    return None

@router.get("/count", response_model=int)
async def count_offers(
    title: Optional[str] = None,
    company: Optional[str] = None,
    location: Optional[str] = None,
    contract_type: Optional[str] = None,
    remote: Optional[bool] = None,
    tech_ids: Optional[List[int]] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Compte le nombre total d'offres d'emploi avec filtres optionnels
    """
    filters = {}
    if title:
        filters["title"] = title
    if company:
        filters["company"] = company
    if location:
        filters["location"] = location
    if contract_type:
        filters["contract_type"] = contract_type
    if remote is not None:
        filters["remote"] = remote
    if tech_ids:
        filters["tech_ids"] = tech_ids
    
    return OfferService.count_offers(db, filters=filters)
