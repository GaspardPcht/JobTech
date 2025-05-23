import os
import requests
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import re

from app.schemas.offer import OfferCreate
from app.schemas.tech import TechCreate

logger = logging.getLogger(__name__)

class AdzunaClient:
    """
    Client pour l'API Adzuna
    Documentation: https://developer.adzuna.com/
    """
    
    BASE_URL = "https://api.adzuna.com/v1/api/jobs"
    
    def _get_mock_data(self, keywords: Optional[str] = None, location: Optional[str] = None) -> Dict[str, Any]:
        """
        Génère des données fictives pour le développement
        """
        mock_results = [
            {
                "id": "1",
                "title": "Développeur Python Senior",
                "description": "Nous recherchons un développeur Python expérimenté pour rejoindre notre équipe. Compétences requises: Python, Django, Flask, PostgreSQL, Docker.",
                "company": {"display_name": "TechCorp"},
                "location": {"display_name": location or "Bordeaux"},
                "salary_min": 45000,
                "salary_max": 60000,
                "contract_type": "permanent",
                "redirect_url": "https://example.com/job/1",
                "created": "2025-05-01T10:00:00"
            },
            {
                "id": "2",
                "title": "Data Scientist",
                "description": "Poste de Data Scientist pour analyse de données. Compétences: Python, TensorFlow, PyTorch, Pandas, SQL.",
                "company": {"display_name": "DataInsight"},
                "location": {"display_name": location or "Bordeaux"},
                "salary_min": 50000,
                "salary_max": 70000,
                "contract_type": "permanent",
                "redirect_url": "https://example.com/job/2",
                "created": "2025-05-02T14:30:00"
            },
            {
                "id": "3",
                "title": "Développeur Frontend React",
                "description": "Développeur frontend pour application web moderne. Compétences: React, TypeScript, JavaScript, HTML, CSS.",
                "company": {"display_name": "WebStudio"},
                "location": {"display_name": location or "Bordeaux"},
                "salary_min": 40000,
                "salary_max": 55000,
                "contract_type": "permanent",
                "redirect_url": "https://example.com/job/3",
                "created": "2025-05-03T09:15:00"
            }
        ]
        
        # Filtrer par mots-clés si spécifiés
        if keywords:
            keywords_lower = keywords.lower()
            filtered_results = []
            for job in mock_results:
                if keywords_lower in job["title"].lower() or keywords_lower in job["description"].lower():
                    filtered_results.append(job)
            mock_results = filtered_results
        
        return {"results": mock_results}
    
    def __init__(self):
        self.app_id = os.getenv("ADZUNA_APP_ID")
        self.app_key = os.getenv("ADZUNA_APP_KEY")
        
        if not self.app_id or not self.app_key:
            logger.warning("Les identifiants API Adzuna ne sont pas configurés")
    
    def search_offers(
        self, 
        keywords: Optional[str] = None,
        location: Optional[str] = None,
        country: str = "fr",
        distance: Optional[int] = None,
        category: Optional[str] = None,
        page: int = 1,
        per_page: int = 20
    ) -> Dict[str, Any]:
        """
        Recherche des offres d'emploi sur Adzuna
        Format de l'API: GET jobs/{country}/search/{page}
        """
        try:
            # Construire l'URL exactement selon la documentation d'Adzuna
            url = f"{self.BASE_URL}/{country}/search/{page}"
            
            # Paramètres de base requis par l'API
            params = {
                "app_id": self.app_id,
                "app_key": self.app_key,
                "results_per_page": per_page
            }
            
            # Ajouter les paramètres optionnels s'ils sont présents
            if keywords:
                params["what"] = keywords
            if location:
                params["where"] = location
            if distance:
                params["distance"] = distance
            if category:
                params["category"] = category
            
            # Supprimer les paramètres None
            params = {k: v for k, v in params.items() if v is not None}
            
            # Afficher l'URL et les paramètres pour le débogage
            logger.info(f"Requête Adzuna: URL={url}, Params={params}")
            
            response = requests.get(url, params=params)
            
            # Afficher la réponse pour le débogage
            logger.info(f"Réponse Adzuna: Status={response.status_code}, URL={response.url}")
            
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Erreur lors de la recherche d'offres Adzuna: {str(e)}")
            # En cas d'erreur, retourner une liste vide au lieu de données fictives
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
                    description=f"Technologie extraite d'Adzuna: {tech}"
                ))
        
        return found_techs
    
    def map_to_offer_schema(self, adzuna_offer: Dict[str, Any]) -> OfferCreate:
        """
        Convertit une offre Adzuna au format de notre application
        """
        # Extraction des technologies mentionnées dans la description
        description = adzuna_offer.get("description", "")
        tech_list = self.extract_technologies(description)
        
        # Déterminer si le poste est en remote
        remote = False
        if "remote" in description.lower() or \
           "télétravail" in description.lower() or \
           "à distance" in description.lower():
            remote = True
        
        # Mapping des types de contrat
        contract_type = "Non précisé"
        contract_info = adzuna_offer.get("contract_type", "").lower()
        if contract_info:
            if "permanent" in contract_info or "cdi" in contract_info:
                contract_type = "CDI"
            elif "temporary" in contract_info or "cdd" in contract_info:
                contract_type = "CDD"
            elif "internship" in contract_info or "stage" in contract_info:
                contract_type = "Stage"
            elif "part_time" in contract_info:
                contract_type = "Temps partiel"
            elif "freelance" in contract_info:
                contract_type = "Freelance"
        
        # Extraction du salaire
        salary_min = None
        salary_max = None
        salary_info = adzuna_offer.get("salary_min")
        if salary_info:
            salary_min = int(salary_info)
        
        salary_info = adzuna_offer.get("salary_max")
        if salary_info:
            salary_max = int(salary_info)
        
        # Création de l'objet OfferCreate
        return OfferCreate(
            title=adzuna_offer.get("title", "Sans titre"),
            company=adzuna_offer.get("company", {}).get("display_name", "Entreprise non précisée"),
            location=adzuna_offer.get("location", {}).get("display_name", "Lieu non précisé"),
            description=description,
            salary_min=salary_min,
            salary_max=salary_max,
            contract_type=contract_type,
            remote=remote,
            url=adzuna_offer.get("redirect_url", ""),
            posted_at=datetime.fromisoformat(adzuna_offer.get("created", datetime.now().isoformat())),
            tech_ids=[],
            techs=tech_list
        )
