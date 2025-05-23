import os
import requests
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import re

from app.schemas.offer import OfferCreate
from app.schemas.tech import TechCreate

logger = logging.getLogger(__name__)

class IndeedClient:
    """
    Client pour l'API Indeed
    Note: Indeed a des restrictions sur son API et nécessite généralement un partenariat.
    Cette implémentation est un exemple et nécessiterait une approche différente en production.
    """
    
    BASE_URL = "https://api.indeed.com/ads/apisearch"
    
    def __init__(self):
        self.publisher_id = os.getenv("INDEED_PUBLISHER_ID")
        
        if not self.publisher_id:
            logger.warning("L'ID d'éditeur Indeed n'est pas configuré")
    
    def search_offers(
        self, 
        keywords: Optional[str] = None,
        location: Optional[str] = None,
        radius: Optional[int] = None,
        job_type: Optional[str] = None,
        page: int = 0,
        per_page: int = 20
    ) -> Dict[str, Any]:
        """
        Recherche des offres d'emploi sur Indeed
        """
        try:
            params = {
                "publisher": self.publisher_id,
                "q": keywords,
                "l": location,
                "radius": radius,
                "jt": job_type,
                "start": page * per_page,
                "limit": per_page,
                "format": "json",
                "v": "2"
            }
            
            # Supprimer les paramètres None
            params = {k: v for k, v in params.items() if v is not None}
            
            response = requests.get(
                self.BASE_URL,
                params=params
            )
            response.raise_for_status()
            
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Erreur lors de la recherche d'offres Indeed: {str(e)}")
            return {"results": []}
    
    def extract_technologies(self, description: str) -> List[TechCreate]:
        """
        Extrait les technologies mentionnées dans la description de l'offre
        en utilisant une liste prédéfinie de technologies courantes
        """
        common_techs = [
            "Python", "JavaScript", "TypeScript", "Java", "C#", "C++", "PHP", "Ruby",
            "Swift", "Kotlin", "Go", "Rust", "React", "Angular", "Vue", "Node.js",
            "Django", "Flask", "Spring", "ASP.NET", "Laravel", "Ruby on Rails",
            "SQL", "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch",
            "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Git", "CI/CD",
            "TensorFlow", "PyTorch", "Pandas", "NumPy", "Scikit-learn"
        ]
        
        found_techs = []
        for tech in common_techs:
            # Recherche du mot entier avec une regex
            pattern = r'\b' + re.escape(tech) + r'\b'
            if re.search(pattern, description, re.IGNORECASE):
                found_techs.append(TechCreate(
                    name=tech,
                    category="Technologie",
                    description=f"Technologie extraite d'Indeed: {tech}"
                ))
        
        return found_techs
    
    def map_to_offer_schema(self, indeed_offer: Dict[str, Any]) -> OfferCreate:
        """
        Convertit une offre Indeed au format de notre application
        """
        # Extraction des technologies mentionnées dans la description
        tech_list = self.extract_technologies(indeed_offer.get("snippet", ""))
        
        # Déterminer si le poste est en remote
        remote = False
        if "remote" in indeed_offer.get("formattedLocationFull", "").lower() or \
           "remote" in indeed_offer.get("snippet", "").lower() or \
           "télétravail" in indeed_offer.get("snippet", "").lower():
            remote = True
        
        # Mapping des types de contrat
        contract_type = "Non précisé"
        if "job_type" in indeed_offer:
            job_type = indeed_offer.get("job_type", "").lower()
            if "full-time" in job_type:
                contract_type = "CDI"
            elif "part-time" in job_type:
                contract_type = "Temps partiel"
            elif "contract" in job_type or "temporary" in job_type:
                contract_type = "CDD"
            elif "internship" in job_type:
                contract_type = "Stage"
        
        # Création de l'objet OfferCreate
        return OfferCreate(
            title=indeed_offer.get("jobtitle", "Sans titre"),
            company=indeed_offer.get("company", "Entreprise non précisée"),
            location=indeed_offer.get("formattedLocationFull", "Lieu non précisé"),
            description=indeed_offer.get("snippet", ""),
            salary_min=None,  # Indeed ne fournit pas toujours des informations structurées sur les salaires
            salary_max=None,
            contract_type=contract_type,
            remote=remote,
            url=indeed_offer.get("url", ""),
            posted_at=datetime.fromtimestamp(int(indeed_offer.get("date", datetime.now().timestamp()))),
            tech_ids=[],
            techs=tech_list
        )
