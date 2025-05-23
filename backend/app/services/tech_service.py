from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional, Dict, Any, Tuple

from app.models import Tech, Offer, offer_tech
from app.schemas.tech import TechCreate, TechUpdate, TechTrend

class TechService:
    """
    Service pour gérer les opérations liées aux technologies
    """
    
    @staticmethod
    def get_techs(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        category: Optional[str] = None
    ) -> List[Tech]:
        """
        Récupère une liste de technologies avec pagination et filtre optionnel par catégorie
        """
        query = db.query(Tech)
        
        if category:
            query = query.filter(Tech.category == category)
        
        # Trier par nom
        query = query.order_by(Tech.name)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_tech(db: Session, tech_id: int) -> Optional[Tech]:
        """
        Récupère une technologie par son ID
        """
        return db.query(Tech).filter(Tech.id == tech_id).first()
    
    @staticmethod
    def get_tech_by_name(db: Session, name: str) -> Optional[Tech]:
        """
        Récupère une technologie par son nom
        """
        return db.query(Tech).filter(func.lower(Tech.name) == func.lower(name)).first()
    
    @staticmethod
    def create_tech(db: Session, tech: TechCreate) -> Tech:
        """
        Crée une nouvelle technologie
        """
        db_tech = Tech(
            name=tech.name,
            category=tech.category,
            description=tech.description
        )
        
        db.add(db_tech)
        db.commit()
        db.refresh(db_tech)
        
        return db_tech
    
    @staticmethod
    def update_tech(db: Session, tech_id: int, tech_data: TechUpdate) -> Optional[Tech]:
        """
        Met à jour une technologie existante
        """
        db_tech = db.query(Tech).filter(Tech.id == tech_id).first()
        if not db_tech:
            return None
        
        # Mettre à jour les champs de la technologie
        tech_data_dict = tech_data.dict(exclude_unset=True)
        
        for key, value in tech_data_dict.items():
            setattr(db_tech, key, value)
        
        db.commit()
        db.refresh(db_tech)
        return db_tech
    
    @staticmethod
    def delete_tech(db: Session, tech_id: int) -> bool:
        """
        Supprime une technologie
        """
        db_tech = db.query(Tech).filter(Tech.id == tech_id).first()
        if not db_tech:
            return False
        
        db.delete(db_tech)
        db.commit()
        return True
    
    @staticmethod
    def get_tech_trends(db: Session, limit: int = 20) -> List[TechTrend]:
        """
        Récupère les tendances des technologies basées sur leur fréquence dans les offres d'emploi
        """
        # Compter le nombre total d'offres
        total_offers = db.query(func.count(Offer.id)).scalar()
        
        if total_offers == 0:
            return []
        
        # Requête pour compter le nombre d'offres par technologie
        tech_counts = db.query(
            Tech.id,
            Tech.name,
            Tech.category,
            func.count(Offer.id).label("count")
        ).join(
            offer_tech
        ).join(
            Offer
        ).group_by(
            Tech.id
        ).order_by(
            desc("count")
        ).limit(limit).all()
        
        # Convertir les résultats en objets TechTrend
        trends = []
        for tech_id, name, category, count in tech_counts:
            percentage = (count / total_offers) * 100
            trends.append(TechTrend(
                name=name,
                category=category,
                count=count,
                percentage=percentage
            ))
        
        return trends
    
    @staticmethod
    def get_techs_with_stats(db: Session) -> List[Tuple[Tech, int]]:
        """
        Récupère toutes les technologies avec le nombre d'offres associées
        """
        return db.query(
            Tech,
            func.count(Offer.id).label("offer_count")
        ).outerjoin(
            offer_tech
        ).outerjoin(
            Offer
        ).group_by(
            Tech.id
        ).order_by(
            desc("offer_count")
        ).all()
