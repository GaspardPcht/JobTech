from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.models.offer import Offer, offer_tech
from app.models import Tech
from app.schemas.offer import OfferCreate, OfferUpdate

def create_offer(db: Session, offer: OfferCreate, tech_ids: List[int] = None) -> Offer:
    """
    Crée une nouvelle offre d'emploi dans la base de données
    """
    # Créer l'offre sans les technologies
    db_offer = Offer(
        title=offer.title,
        company=offer.company,
        location=offer.location,
        description=offer.description,
        salary_min=offer.salary_min,
        salary_max=offer.salary_max,
        contract_type=offer.contract_type,
        remote=offer.remote,
        url=offer.url,
        posted_at=datetime.utcnow(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    db.add(db_offer)
    db.commit()
    db.refresh(db_offer)
    
    # Ajouter les technologies si spécifiées
    if tech_ids:
        # Récupérer les technologies par leurs IDs
        techs = db.query(Tech).filter(Tech.id.in_(tech_ids)).all() if tech_ids else []
        db_offer.techs = techs
        db.commit()
        db.refresh(db_offer)
    
    return db_offer

def get_offer_by_id(db: Session, offer_id: int) -> Optional[Offer]:
    """
    Récupère une offre d'emploi par son ID
    """
    return db.query(Offer).filter(Offer.id == offer_id).first()

def get_offer_by_url(db: Session, url: str) -> Optional[Offer]:
    """
    Récupère une offre d'emploi par son URL
    """
    return db.query(Offer).filter(Offer.url == url).first()

def get_offers(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    keywords: Optional[str] = None,
    location: Optional[str] = None,
    contract_type: Optional[str] = None,
    remote: Optional[bool] = None
) -> List[Offer]:
    """
    Récupère une liste d'offres d'emploi avec filtrage optionnel
    """
    query = db.query(Offer)
    
    # Appliquer les filtres si spécifiés
    if keywords:
        query = query.filter(
            (Offer.title.ilike(f"%{keywords}%")) | 
            (Offer.description.ilike(f"%{keywords}%"))
        )
    
    if location:
        query = query.filter(Offer.location.ilike(f"%{location}%"))
    
    if contract_type:
        query = query.filter(Offer.contract_type == contract_type)
    
    if remote is not None:
        query = query.filter(Offer.remote == remote)
    
    # Trier par date de publication (la plus récente en premier)
    query = query.order_by(Offer.posted_at.desc())
    
    return query.offset(skip).limit(limit).all()

def update_offer(db: Session, offer_id: int, offer_update: OfferUpdate) -> Optional[Offer]:
    """
    Met à jour une offre d'emploi existante
    """
    db_offer = get_offer_by_id(db, offer_id)
    if not db_offer:
        return None
    
    # Mettre à jour les champs spécifiés
    update_data = offer_update.dict(exclude_unset=True)
    
    # Gérer séparément les technologies
    tech_ids = update_data.pop("tech_ids", None)
    
    for key, value in update_data.items():
        setattr(db_offer, key, value)
    
    # Mettre à jour la date de modification
    db_offer.updated_at = datetime.utcnow()
    
    # Mettre à jour les technologies si spécifiées
    if tech_ids is not None:
        # Récupérer les technologies par leurs IDs
        techs = db.query(Tech).filter(Tech.id.in_(tech_ids)).all() if tech_ids else []
        db_offer.techs = techs
    
    db.commit()
    db.refresh(db_offer)
    return db_offer

def delete_offer(db: Session, offer_id: int) -> bool:
    """
    Supprime une offre d'emploi
    """
    db_offer = get_offer_by_id(db, offer_id)
    if not db_offer:
        return False
    
    db.delete(db_offer)
    db.commit()
    return True

def create_or_update_external_offer(db: Session, offer_data: dict) -> Offer:
    """
    Crée ou met à jour une offre externe dans la base de données
    """
    # Vérifier si l'offre existe déjà par son URL
    existing_offer = get_offer_by_url(db, offer_data.get("url"))
    
    if existing_offer:
        # Mettre à jour l'offre existante
        for key, value in offer_data.items():
            if key != "techs" and hasattr(existing_offer, key):
                setattr(existing_offer, key, value)
        
        existing_offer.updated_at = datetime.utcnow()
        
        # Gérer les technologies si présentes
        if "techs" in offer_data and offer_data["techs"]:
            tech_ids = [tech.id for tech in offer_data["techs"]]
            # Récupérer les technologies par leurs IDs
            techs = db.query(Tech).filter(Tech.id.in_(tech_ids)).all() if tech_ids else []
            existing_offer.techs = techs
        
        db.commit()
        db.refresh(existing_offer)
        return existing_offer
    else:
        # Créer une nouvelle offre
        techs = []
        if "techs" in offer_data:
            techs = offer_data.pop("techs", [])
        
        db_offer = Offer(**{k: v for k, v in offer_data.items() if hasattr(Offer, k)})
        
        db.add(db_offer)
        db.commit()
        db.refresh(db_offer)
        
        # Ajouter les technologies si présentes
        if techs:
            tech_ids = [tech.id for tech in techs]
            # Récupérer les technologies par leurs IDs
            db_techs = db.query(Tech).filter(Tech.id.in_(tech_ids)).all() if tech_ids else []
            db_offer.techs = db_techs
            db.commit()
            db.refresh(db_offer)
        
        return db_offer
