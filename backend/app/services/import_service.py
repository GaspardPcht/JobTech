from sqlalchemy.orm import Session
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.integrations.pole_emploi import PoleEmploiClient
from app.integrations.adzuna import AdzunaClient
from app.integrations.linkedin import LinkedInClient
from app.services.offer_service import OfferService
from app.services.tech_service import TechService
from app.schemas.offer import OfferCreate
from app.schemas.tech import TechCreate

logger = logging.getLogger(__name__)

class ImportService:
    """
    Service pour importer des offres d'emploi depuis différentes sources externes
    """
    
    @staticmethod
    def is_pole_emploi_configured() -> bool:
        """
        Vérifie si l'API Pôle Emploi est configurée
        """
        client = PoleEmploiClient()
        return client.client_id is not None and client.client_secret is not None
    
    @staticmethod
    def is_adzuna_configured() -> bool:
        """
        Vérifie si l'API Adzuna est configurée
        """
        client = AdzunaClient()
        return client.app_id is not None and client.app_key is not None
    
    @staticmethod
    async def import_from_pole_emploi(
        db: Session,
        keywords: Optional[str] = None,
        location: Optional[str] = None,
        distance: Optional[int] = None,
        contract_type: Optional[str] = None,
        max_offers: int = 100
    ) -> int:
        """
        Importe des offres d'emploi depuis Pôle Emploi
        Retourne le nombre d'offres importées
        """
        client = PoleEmploiClient()
        imported_count = 0
        page = 0
        per_page = 20
        
        while imported_count < max_offers:
            # Recherche des offres
            results = client.search_offers(
                keywords=keywords,
                location=location,
                distance=distance,
                contract_type=contract_type,
                page=page,
                per_page=per_page
            )
            
            offers = results.get("resultats", [])
            if not offers:
                break
                
            # Traitement des offres
            for offer_data in offers:
                if imported_count >= max_offers:
                    break
                    
                try:
                    # Récupérer plus de détails si nécessaire
                    offer_id = offer_data.get("id")
                    if offer_id:
                        details = client.get_offer_details(offer_id)
                        if details:
                            offer_data.update(details)
                    
                    # Convertir au format de notre application
                    offer_create = client.map_to_offer_schema(offer_data)
                    
                    # Créer ou récupérer les technologies
                    tech_ids = []
                    for tech in offer_create.techs:
                        db_tech = TechService.get_tech_by_name(db, tech.name)
                        if not db_tech:
                            db_tech = TechService.create_tech(db, tech)
                        tech_ids.append(db_tech.id)
                    
                    # Mettre à jour les IDs des technologies
                    offer_create.tech_ids = tech_ids
                    
                    # Vérifier si l'offre existe déjà (par URL ou titre+entreprise)
                    existing_offer = None
                    if offer_create.url:
                        existing_offer = OfferService.get_offer_by_url(db, offer_create.url)
                    
                    if not existing_offer and offer_create.title and offer_create.company:
                        existing_offer = OfferService.get_offer_by_title_and_company(
                            db, 
                            offer_create.title, 
                            offer_create.company
                        )
                    
                    # Créer ou mettre à jour l'offre
                    if not existing_offer:
                        OfferService.create_offer(db, offer_create)
                        imported_count += 1
                        logger.info(f"Offre importée: {offer_create.title} - {offer_create.company}")
                    else:
                        logger.info(f"Offre déjà existante: {offer_create.title} - {offer_create.company}")
                
                except Exception as e:
                    logger.error(f"Erreur lors de l'importation d'une offre Pôle Emploi: {str(e)}")
            
            # Passer à la page suivante
            page += 1
            
            # Si on a reçu moins d'offres que demandé, c'est qu'il n'y en a plus
            if len(offers) < per_page:
                break
        
        return imported_count
    
    @staticmethod
    async def import_from_adzuna(
        db: Session,
        keywords: Optional[str] = None,
        location: Optional[str] = None,
        country: str = "fr",
        distance: Optional[int] = None,
        category: Optional[str] = None,
        max_offers: int = 100
    ) -> int:
        """
        Importe des offres d'emploi depuis Adzuna
        Retourne le nombre d'offres importées
        """
        client = AdzunaClient()
        imported_count = 0
        page = 1  # Adzuna commence à la page 1
        per_page = 20
        
        while imported_count < max_offers:
            # Recherche des offres
            results = client.search_offers(
                keywords=keywords,
                location=location,
                country=country,
                distance=distance,
                category=category,
                page=page,
                per_page=per_page
            )
            
            offers = results.get("results", [])
            if not offers:
                break
                
            # Traitement des offres
            for offer_data in offers:
                if imported_count >= max_offers:
                    break
                    
                try:
                    # Convertir au format de notre application
                    offer_create = client.map_to_offer_schema(offer_data)
                    
                    # Créer ou récupérer les technologies
                    tech_ids = []
                    for tech in offer_create.techs:
                        db_tech = TechService.get_tech_by_name(db, tech.name)
                        if not db_tech:
                            db_tech = TechService.create_tech(db, tech)
                        tech_ids.append(db_tech.id)
                    
                    # Mettre à jour les IDs des technologies
                    offer_create.tech_ids = tech_ids
                    
                    # Vérifier si l'offre existe déjà (par URL ou titre+entreprise)
                    existing_offer = None
                    if offer_create.url:
                        existing_offer = OfferService.get_offer_by_url(db, offer_create.url)
                    
                    if not existing_offer and offer_create.title and offer_create.company:
                        existing_offer = OfferService.get_offer_by_title_and_company(
                            db, 
                            offer_create.title, 
                            offer_create.company
                        )
                    
                    # Créer ou mettre à jour l'offre
                    if not existing_offer:
                        OfferService.create_offer(db, offer_create)
                        imported_count += 1
                        logger.info(f"Offre importée: {offer_create.title} - {offer_create.company}")
                    else:
                        logger.info(f"Offre déjà existante: {offer_create.title} - {offer_create.company}")
                
                except Exception as e:
                    logger.error(f"Erreur lors de l'importation d'une offre Adzuna: {str(e)}")
            
            # Passer à la page suivante
            page += 1
            
            # Si on a reçu moins d'offres que demandé, c'est qu'il n'y en a plus
            if len(offers) < per_page:
                break
        
        return imported_count
    
    @staticmethod
    async def import_from_all_sources(
        db: Session,
        keywords: Optional[str] = None,
        location: Optional[str] = None,
        max_offers_per_source: int = 50
    ) -> Dict[str, int]:
        """
        Importe des offres d'emploi depuis toutes les sources configurées
        Retourne le nombre d'offres importées par source
        """
        results = {}
        
        # Import depuis Pôle Emploi
        try:
            pole_emploi_count = await ImportService.import_from_pole_emploi(
                db=db,
                keywords=keywords,
                location=location,
                max_offers=max_offers_per_source
            )
            results["pole_emploi"] = pole_emploi_count
        except Exception as e:
            logger.error(f"Erreur lors de l'import depuis Pôle Emploi: {str(e)}")
            results["pole_emploi"] = 0
        
        # Import depuis Adzuna
        try:
            adzuna_count = await ImportService.import_from_adzuna(
                db=db,
                keywords=keywords,
                location=location,
                country="fr",  # France par défaut
                max_offers=max_offers_per_source
            )
            results["adzuna"] = adzuna_count
        except Exception as e:
            logger.error(f"Erreur lors de l'import depuis Adzuna: {str(e)}")
            results["adzuna"] = 0
        
        # Autres sources à ajouter ici...
        
        return results
