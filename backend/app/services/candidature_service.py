from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.models import Candidature, Offer, CandidatureStatus
from app.schemas.candidature import CandidatureCreate, CandidatureUpdate

class CandidatureService:
    """
    Service pour gérer les opérations liées aux candidatures
    """
    
    @staticmethod
    def get_candidatures(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Candidature]:
        """
        Récupère une liste de candidatures avec pagination et filtres optionnels
        """
        query = db.query(Candidature)
        
        # Appliquer les filtres si fournis
        if filters:
            if filters.get("status"):
                query = query.filter(Candidature.status == filters["status"])
            if filters.get("offer_id"):
                query = query.filter(Candidature.offer_id == filters["offer_id"])
            if filters.get("date_from"):
                query = query.filter(Candidature.application_date >= filters["date_from"])
            if filters.get("date_to"):
                query = query.filter(Candidature.application_date <= filters["date_to"])
        
        # Trier par date de mise à jour (plus récent d'abord)
        query = query.order_by(desc(Candidature.updated_at))
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_candidature(db: Session, candidature_id: int) -> Optional[Candidature]:
        """
        Récupère une candidature par son ID
        """
        return db.query(Candidature).filter(Candidature.id == candidature_id).first()
    
    @staticmethod
    def create_candidature(db: Session, candidature: CandidatureCreate) -> Candidature:
        """
        Crée une nouvelle candidature
        """
        # Vérifier si l'offre existe
        offer = db.query(Offer).filter(Offer.id == candidature.offer_id).first()
        if not offer:
            raise ValueError(f"L'offre avec l'ID {candidature.offer_id} n'existe pas")
        
        # Créer l'objet candidature
        db_candidature = Candidature(
            offer_id=candidature.offer_id,
            status=candidature.status,
            application_date=candidature.application_date or datetime.utcnow(),
            notes=candidature.notes,
            next_step=candidature.next_step,
            next_step_date=candidature.next_step_date
        )
        
        db.add(db_candidature)
        db.commit()
        db.refresh(db_candidature)
        
        return db_candidature
    
    @staticmethod
    def update_candidature(
        db: Session, 
        candidature_id: int, 
        candidature_data: CandidatureUpdate
    ) -> Optional[Candidature]:
        """
        Met à jour une candidature existante
        """
        db_candidature = db.query(Candidature).filter(Candidature.id == candidature_id).first()
        if not db_candidature:
            return None
        
        # Mettre à jour les champs de la candidature
        candidature_data_dict = candidature_data.dict(exclude_unset=True)
        
        for key, value in candidature_data_dict.items():
            setattr(db_candidature, key, value)
        
        db.commit()
        db.refresh(db_candidature)
        return db_candidature
    
    @staticmethod
    def delete_candidature(db: Session, candidature_id: int) -> bool:
        """
        Supprime une candidature
        """
        db_candidature = db.query(Candidature).filter(Candidature.id == candidature_id).first()
        if not db_candidature:
            return False
        
        db.delete(db_candidature)
        db.commit()
        return True
    
    @staticmethod
    def get_candidature_stats(db: Session) -> Dict[str, int]:
        """
        Récupère des statistiques sur les candidatures par statut
        """
        stats = {}
        
        # Compter le nombre de candidatures par statut
        status_counts = db.query(
            Candidature.status,
            func.count(Candidature.id)
        ).group_by(
            Candidature.status
        ).all()
        
        # Initialiser tous les statuts à 0
        for status in CandidatureStatus:
            stats[status.value] = 0
        
        # Mettre à jour avec les valeurs réelles
        for status, count in status_counts:
            stats[status.value] = count
        
        # Ajouter le total
        stats["total"] = sum(stats.values())
        
        return stats
