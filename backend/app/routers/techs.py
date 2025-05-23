from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.services.tech_service import TechService
from app.schemas.tech import TechCreate, TechUpdate, TechInDB, TechWithStats, TechTrend

router = APIRouter(
    prefix="/techs",
    tags=["techs"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[TechInDB])
async def read_techs(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Récupère une liste de technologies avec pagination et filtre optionnel par catégorie
    """
    techs = TechService.get_techs(db, skip=skip, limit=limit, category=category)
    return techs

@router.get("/stats", response_model=List[TechWithStats])
async def read_techs_with_stats(db: Session = Depends(get_db)):
    """
    Récupère toutes les technologies avec le nombre d'offres associées
    """
    techs_with_stats = TechService.get_techs_with_stats(db)
    result = []
    for tech, offer_count in techs_with_stats:
        tech_dict = TechInDB.from_orm(tech).dict()
        tech_dict["offer_count"] = offer_count
        result.append(TechWithStats(**tech_dict))
    return result

@router.get("/trends", response_model=List[TechTrend])
async def read_tech_trends(limit: int = 20, db: Session = Depends(get_db)):
    """
    Récupère les tendances des technologies basées sur leur fréquence dans les offres d'emploi
    """
    return TechService.get_tech_trends(db, limit=limit)

@router.get("/{tech_id}", response_model=TechInDB)
async def read_tech(tech_id: int, db: Session = Depends(get_db)):
    """
    Récupère une technologie spécifique par son ID
    """
    tech = TechService.get_tech(db, tech_id=tech_id)
    if tech is None:
        raise HTTPException(status_code=404, detail="Technologie non trouvée")
    return tech

@router.post("/", response_model=TechInDB, status_code=status.HTTP_201_CREATED)
async def create_tech(tech: TechCreate, db: Session = Depends(get_db)):
    """
    Crée une nouvelle technologie
    """
    # Vérifier si la technologie existe déjà
    db_tech = TechService.get_tech_by_name(db, name=tech.name)
    if db_tech:
        raise HTTPException(
            status_code=400,
            detail=f"Une technologie avec le nom '{tech.name}' existe déjà"
        )
    return TechService.create_tech(db=db, tech=tech)

@router.put("/{tech_id}", response_model=TechInDB)
async def update_tech(tech_id: int, tech: TechUpdate, db: Session = Depends(get_db)):
    """
    Met à jour une technologie existante
    """
    # Vérifier si le nouveau nom existe déjà (s'il est fourni)
    if tech.name:
        existing_tech = TechService.get_tech_by_name(db, name=tech.name)
        if existing_tech and existing_tech.id != tech_id:
            raise HTTPException(
                status_code=400,
                detail=f"Une technologie avec le nom '{tech.name}' existe déjà"
            )
    
    updated_tech = TechService.update_tech(db=db, tech_id=tech_id, tech_data=tech)
    if updated_tech is None:
        raise HTTPException(status_code=404, detail="Technologie non trouvée")
    return updated_tech

@router.delete("/{tech_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tech(tech_id: int, db: Session = Depends(get_db)):
    """
    Supprime une technologie
    """
    success = TechService.delete_tech(db=db, tech_id=tech_id)
    if not success:
        raise HTTPException(status_code=404, detail="Technologie non trouvée")
    return None
