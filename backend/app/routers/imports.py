from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Optional

from app.database import get_db
from app.services.import_service import ImportService

router = APIRouter(
    prefix="/imports",
    tags=["imports"],
    responses={404: {"description": "Not found"}},
)

@router.post("/pole-emploi", status_code=status.HTTP_202_ACCEPTED)
async def import_from_pole_emploi(
    background_tasks: BackgroundTasks,
    keywords: Optional[str] = None,
    location: Optional[str] = None,
    distance: Optional[int] = None,
    contract_type: Optional[str] = None,
    max_offers: int = 50,
    db: Session = Depends(get_db)
):
    """
    Importe des offres d'emploi depuis l'API Pôle Emploi
    Cette opération s'exécute en arrière-plan
    """
    # Vérifier si les identifiants API sont configurés
    if not ImportService.is_pole_emploi_configured():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="L'API Pôle Emploi n'est pas configurée. Veuillez définir POLE_EMPLOI_CLIENT_ID et POLE_EMPLOI_CLIENT_SECRET dans les variables d'environnement."
        )
    
    # Ajouter la tâche d'importation en arrière-plan
    background_tasks.add_task(
        ImportService.import_from_pole_emploi,
        db=db,
        keywords=keywords,
        location=location,
        distance=distance,
        contract_type=contract_type,
        max_offers=max_offers
    )
    
    return {"message": "Importation des offres Pôle Emploi lancée en arrière-plan"}

@router.post("/adzuna", status_code=status.HTTP_202_ACCEPTED)
async def import_from_adzuna(
    background_tasks: BackgroundTasks,
    keywords: Optional[str] = None,
    location: Optional[str] = None,
    country: str = "fr",
    distance: Optional[int] = None,
    category: Optional[str] = None,
    max_offers: int = 50,
    db: Session = Depends(get_db)
):
    """
    Importe des offres d'emploi depuis l'API Adzuna
    Cette opération s'exécute en arrière-plan
    """
    # Vérifier si les identifiants API sont configurés
    if not ImportService.is_adzuna_configured():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="L'API Adzuna n'est pas configurée. Veuillez définir ADZUNA_APP_ID et ADZUNA_APP_KEY dans les variables d'environnement."
        )
    
    # Ajouter la tâche d'importation en arrière-plan
    background_tasks.add_task(
        ImportService.import_from_adzuna,
        db=db,
        keywords=keywords,
        location=location,
        country=country,
        distance=distance,
        category=category,
        max_offers=max_offers
    )
    
    return {"message": "Importation des offres Adzuna lancée en arrière-plan"}

@router.post("/all", status_code=status.HTTP_202_ACCEPTED)
async def import_from_all_sources(
    background_tasks: BackgroundTasks,
    keywords: Optional[str] = None,
    location: Optional[str] = None,
    max_offers_per_source: int = 30,
    db: Session = Depends(get_db)
):
    """
    Importe des offres d'emploi depuis toutes les sources configurées
    Cette opération s'exécute en arrière-plan
    """
    # Ajouter la tâche d'importation en arrière-plan
    background_tasks.add_task(
        ImportService.import_from_all_sources,
        db=db,
        keywords=keywords,
        location=location,
        max_offers_per_source=max_offers_per_source
    )
    
    return {"message": "Importation des offres depuis toutes les sources lancée en arrière-plan"}
