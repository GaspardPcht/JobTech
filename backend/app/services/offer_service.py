from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.models.offer import Offer, offer_tech
from app.models.tech import Tech
from app.schemas.offer import OfferCreate, OfferUpdate, OfferResponse
from app.schemas.tech import TechBase

class OfferService:
    """
    Service pour gérer les opérations liées aux offres d'emploi
    """
    
    @staticmethod
    def get_offers(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[OfferResponse]:
        """
        Récupère une liste d'offres d'emploi avec pagination et filtres optionnels
        """
        query = db.query(Offer)
        
        # Appliquer les filtres si fournis
        if filters:
            if filters.get("title"):
                query = query.filter(Offer.title.ilike(f"%{filters['title']}%"))
            if filters.get("company"):
                query = query.filter(Offer.company.ilike(f"%{filters['company']}%"))
            if filters.get("location"):
                query = query.filter(Offer.location.ilike(f"%{filters['location']}%"))
            if filters.get("contract_type"):
                query = query.filter(Offer.contract_type == filters["contract_type"])
            if filters.get("remote") is not None:
                query = query.filter(Offer.remote == filters["remote"])
            if filters.get("tech_ids"):
                query = query.join(offer_tech).join(Tech).filter(
                    Tech.id.in_(filters["tech_ids"])
                ).group_by(Offer.id).having(
                    func.count(Tech.id) == len(filters["tech_ids"])
                )
            if filters.get("min_salary"):
                query = query.filter(Offer.salary_min >= filters["min_salary"])
            if filters.get("max_salary"):
                query = query.filter(Offer.salary_max <= filters["max_salary"])
        
        # Trier par date de publication (plus récent d'abord)
        query = query.order_by(desc(Offer.posted_at))
        
        # Récupérer les offres avec pagination
        offers = query.offset(skip).limit(limit).all()
        
        # Convertir les offres en schémas Pydantic
        result = []
        for offer in offers:
            # Convertir les technologies en schémas TechBase
            tech_schemas = []
            for tech in offer.techs:
                if hasattr(tech, 'id') and tech.id is not None:
                    tech_schemas.append(TechBase(
                        id=tech.id,
                        name=tech.name,
                        category=tech.category,
                        description=tech.description
                    ))
                # Si une technologie n'a pas d'ID, on ne l'ajoute pas pour éviter les erreurs de validation
            
            # Créer le schéma OfferResponse
            offer_response = OfferResponse(
                id=offer.id,
                title=offer.title,
                company=offer.company,
                location=offer.location,
                description=offer.description,
                salary_min=offer.salary_min,
                salary_max=offer.salary_max,
                contract_type=offer.contract_type,
                remote=offer.remote,
                url=offer.url,
                posted_at=offer.posted_at,
                created_at=offer.created_at,
                updated_at=offer.updated_at,
                techs=tech_schemas
            )
            result.append(offer_response)
        
        return result
    
    @staticmethod
    def get_offer(db: Session, offer_id: int) -> Optional[OfferResponse]:
        """
        Récupère une offre d'emploi par son ID
        """
        offer = db.query(Offer).filter(Offer.id == offer_id).first()
        
        if not offer:
            return None
            
        # Convertir les technologies en schémas TechBase
        tech_schemas = []
        for tech in offer.techs:
            if hasattr(tech, 'id') and tech.id is not None:
                tech_schemas.append(TechBase(
                    id=tech.id,
                    name=tech.name,
                    category=tech.category,
                    description=tech.description
                ))
            # Si une technologie n'a pas d'ID, on ne l'ajoute pas pour éviter les erreurs de validation
        
        # Créer le schéma OfferResponse
        return OfferResponse(
            id=offer.id,
            title=offer.title,
            company=offer.company,
            location=offer.location,
            description=offer.description,
            salary_min=offer.salary_min,
            salary_max=offer.salary_max,
            contract_type=offer.contract_type,
            remote=offer.remote,
            url=offer.url,
            posted_at=offer.posted_at,
            created_at=offer.created_at,
            updated_at=offer.updated_at,
            techs=tech_schemas
        )
    
    @staticmethod
    def create_offer(db: Session, offer: OfferCreate) -> OfferResponse:
        """
        Crée une nouvelle offre d'emploi
        """
        # Extraire les IDs de technologies de l'offre
        tech_ids = offer.tech_ids
        
        # Créer l'objet d'offre sans les technologies
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
            posted_at=datetime.utcnow()
        )
        
        db.add(db_offer)
        db.commit()
        db.refresh(db_offer)
        
        # Ajouter les technologies à l'offre
        techs = []
        if tech_ids:
            techs = db.query(Tech).filter(Tech.id.in_(tech_ids)).all()
            db_offer.techs = techs
            db.commit()
            db.refresh(db_offer)
        
        # Convertir les technologies en schémas TechBase
        tech_schemas = []
        for tech in techs:
            if hasattr(tech, 'id') and tech.id is not None:
                tech_schemas.append(TechBase(
                    id=tech.id,
                    name=tech.name,
                    category=tech.category,
                    description=tech.description
                ))
            # Si une technologie n'a pas d'ID, on ne l'ajoute pas pour éviter les erreurs de validation
        
        # Créer le schéma OfferResponse
        return OfferResponse(
            id=db_offer.id,
            title=db_offer.title,
            company=db_offer.company,
            location=db_offer.location,
            description=db_offer.description,
            salary_min=db_offer.salary_min,
            salary_max=db_offer.salary_max,
            contract_type=db_offer.contract_type,
            remote=db_offer.remote,
            url=db_offer.url,
            posted_at=db_offer.posted_at,
            created_at=db_offer.created_at,
            updated_at=db_offer.updated_at,
            techs=tech_schemas
        )
    
    @staticmethod
    def update_offer(db: Session, offer_id: int, offer_data: OfferUpdate) -> Optional[OfferResponse]:
        """
        Met à jour une offre d'emploi existante
        """
        db_offer = db.query(Offer).filter(Offer.id == offer_id).first()
        if not db_offer:
            return None
        
        # Mettre à jour les champs de l'offre
        offer_data_dict = offer_data.dict(exclude_unset=True)
        tech_ids = offer_data_dict.pop("tech_ids", None)
        
        for key, value in offer_data_dict.items():
            setattr(db_offer, key, value)
        
        # Mettre à jour les technologies si fournies
        if tech_ids is not None:
            techs = db.query(Tech).filter(Tech.id.in_(tech_ids)).all()
            db_offer.techs = techs
        
        db.commit()
        db.refresh(db_offer)
        
        # Convertir les technologies en schémas TechBase
        tech_schemas = []
        for tech in db_offer.techs:
            if hasattr(tech, 'id') and tech.id is not None:
                tech_schemas.append(TechBase(
                    id=tech.id,
                    name=tech.name,
                    category=tech.category,
                    description=tech.description
                ))
            # Si une technologie n'a pas d'ID, on ne l'ajoute pas pour éviter les erreurs de validation
        
        # Créer le schéma OfferResponse
        return OfferResponse(
            id=db_offer.id,
            title=db_offer.title,
            company=db_offer.company,
            location=db_offer.location,
            description=db_offer.description,
            salary_min=db_offer.salary_min,
            salary_max=db_offer.salary_max,
            contract_type=db_offer.contract_type,
            remote=db_offer.remote,
            url=db_offer.url,
            posted_at=db_offer.posted_at,
            created_at=db_offer.created_at,
            updated_at=db_offer.updated_at,
            techs=tech_schemas
        )
    
    @staticmethod
    def delete_offer(db: Session, offer_id: int) -> bool:
        """
        Supprime une offre d'emploi
        """
        db_offer = db.query(Offer).filter(Offer.id == offer_id).first()
        if not db_offer:
            return False
        
        db.delete(db_offer)
        db.commit()
        return True
    
    @staticmethod
    def count_offers(db: Session, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        Compte le nombre total d'offres d'emploi avec filtres optionnels
        """
        query = db.query(func.count(Offer.id))
        
        # Appliquer les filtres si fournis
        if filters:
            if filters.get("title"):
                query = query.filter(Offer.title.ilike(f"%{filters['title']}%"))
            if filters.get("company"):
                query = query.filter(Offer.company.ilike(f"%{filters['company']}%"))
            if filters.get("location"):
                query = query.filter(Offer.location.ilike(f"%{filters['location']}%"))
            if filters.get("contract_type"):
                query = query.filter(Offer.contract_type == filters["contract_type"])
            if filters.get("remote") is not None:
                query = query.filter(Offer.remote == filters["remote"])
            if filters.get("tech_ids"):
                query = query.join(offer_tech).join(Tech).filter(
                    Tech.id.in_(filters["tech_ids"])
                ).group_by(Offer.id).having(
                    func.count(Tech.id) == len(filters["tech_ids"])
                )
        
        return query.scalar()
    
    @staticmethod
    def get_offer_by_url(db: Session, url: str) -> Optional[Offer]:
        """
        Récupère une offre d'emploi par son URL
        Utile pour éviter les doublons lors de l'importation depuis des sources externes
        """
        return db.query(Offer).filter(Offer.url == url).first()
    
    @staticmethod
    def get_offer_by_title_and_company(db: Session, title: str, company: str) -> Optional[Offer]:
        """
        Récupère une offre d'emploi par son titre et son entreprise
        Utile pour éviter les doublons lors de l'importation depuis des sources externes
        """
        return db.query(Offer).filter(
            Offer.title.ilike(f"%{title}%"),
            Offer.company.ilike(f"%{company}%")
        ).first()
