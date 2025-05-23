import os
import requests
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

from app.schemas.offer import OfferCreate
from app.schemas.tech import TechCreate

logger = logging.getLogger(__name__)

class PoleEmploiClient:
    """
    Client pour l'API Emploi Store de Pôle Emploi
    Documentation: https://www.emploi-store-dev.fr/portail-developpeur/catalogueapi
    """
    
    BASE_URL = "https://api.emploi-store.fr/partenaire/offresdemploi/v2"
    AUTH_URL = "https://entreprise.pole-emploi.fr/connexion/oauth2/access_token"
    
    def _get_mock_data(self, keywords: Optional[str] = None, location: Optional[str] = None) -> Dict[str, Any]:
        """
        Génère des données fictives pour le développement
        """
        mock_results = [
            {
                "id": "101",
                "intitule": "Ingénieur DevOps",
                "description": "Nous recherchons un ingénieur DevOps pour notre équipe technique. Compétences: Docker, Kubernetes, AWS, CI/CD, Git.",
                "entreprise": {"nom": "CloudTech"},
                "lieuTravail": {"libelle": location or "Bordeaux"},
                "typeContrat": "CDI",
                "salaire": {"libelle": "45000 - 60000 EUR par an"},
                "origineOffre": {"urlOrigine": "https://example.com/job/101"},
                "competences": [
                    {"libelle": "Docker"},
                    {"libelle": "Kubernetes"},
                    {"libelle": "AWS"},
                    {"libelle": "CI/CD"}
                ]
            },
            {
                "id": "102",
                "intitule": "Développeur Full Stack",
                "description": "Développeur Full Stack pour application web. Compétences: JavaScript, Node.js, React, MongoDB, Express.",
                "entreprise": {"nom": "WebSolutions"},
                "lieuTravail": {"libelle": location or "Bordeaux"},
                "typeContrat": "CDI",
                "salaire": {"libelle": "40000 - 55000 EUR par an"},
                "origineOffre": {"urlOrigine": "https://example.com/job/102"},
                "competences": [
                    {"libelle": "JavaScript"},
                    {"libelle": "Node.js"},
                    {"libelle": "React"},
                    {"libelle": "MongoDB"}
                ]
            },
            {
                "id": "103",
                "intitule": "Data Engineer",
                "description": "Ingénieur de données pour notre plateforme d'analyse. Compétences: Python, Spark, Hadoop, SQL, ETL.",
                "entreprise": {"nom": "DataFlow"},
                "lieuTravail": {"libelle": location or "Bordeaux"},
                "typeContrat": "CDI",
                "salaire": {"libelle": "50000 - 65000 EUR par an"},
                "origineOffre": {"urlOrigine": "https://example.com/job/103"},
                "competences": [
                    {"libelle": "Python"},
                    {"libelle": "Spark"},
                    {"libelle": "Hadoop"},
                    {"libelle": "SQL"}
                ]
            }
        ]
        
        # Filtrer par mots-clés si spécifiés
        if keywords:
            keywords_lower = keywords.lower()
            filtered_results = []
            for job in mock_results:
                if keywords_lower in job["intitule"].lower() or keywords_lower in job["description"].lower():
                    filtered_results.append(job)
            mock_results = filtered_results
        
        return {"resultats": mock_results}
    
    def __init__(self):
        self.client_id = os.getenv("POLE_EMPLOI_CLIENT_ID")
        self.client_secret = os.getenv("POLE_EMPLOI_CLIENT_SECRET")
        self.access_token = None
        self.token_expiry = datetime.now()
        
        if not self.client_id or not self.client_secret:
            logger.warning("Les identifiants API Pôle Emploi ne sont pas configurés")
    
    def _authenticate(self) -> None:
        """
        Obtient un token d'accès pour l'API Pôle Emploi
        """
        if self.access_token and self.token_expiry > datetime.now():
            return
            
        try:
            # Format exact selon la documentation Pôle Emploi
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            data = {
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'scope': 'api_offresdemploiv2 o2dsoffre'  # Scope pour l'API des offres d'emploi
            }
            
            # Afficher les données pour le débogage
            logger.info(f"Requête d'authentification Pôle Emploi: URL={self.AUTH_URL}/access_token, Data={data}")
            
            response = requests.post(
                f"{self.AUTH_URL}/access_token",
                headers=headers,
                data=data
            )
            
            # Afficher la réponse pour le débogage
            logger.info(f"Réponse d'authentification Pôle Emploi: Status={response.status_code}")
            
            response.raise_for_status()
            
            data = response.json()
            self.access_token = data.get("access_token")
            expires_in = data.get("expires_in", 3600)  # Par défaut 1 heure
            self.token_expiry = datetime.now() + timedelta(seconds=expires_in)
            
            logger.info("Authentification à l'API Pôle Emploi réussie")
        except requests.RequestException as e:
            logger.error(f"Erreur lors de l'authentification à l'API Pôle Emploi: {str(e)}")
            raise
    
    def _get_headers(self) -> Dict[str, str]:
        """
        Retourne les en-têtes pour les requêtes à l'API
        """
        self._authenticate()
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def search_offers(
        self, 
        keywords: Optional[str] = None,
        location: Optional[str] = None,
        distance: Optional[int] = None,
        contract_type: Optional[str] = None,
        page: int = 0,
        per_page: int = 20
    ) -> Dict[str, Any]:
        """
        Recherche des offres d'emploi selon les critères spécifiés
        """
        try:
            params = {
                "motsCles": keywords,
                "commune": location,
                "distance": distance,
                "typeContrat": contract_type,
                "range": f"{page * per_page}-{(page + 1) * per_page - 1}"
            }
            
            # Supprimer les paramètres None
            params = {k: v for k, v in params.items() if v is not None}
            
            response = requests.get(
                f"{self.BASE_URL}/offres/search",
                headers=self._get_headers(),
                params=params
            )
            response.raise_for_status()
            
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Erreur lors de la recherche d'offres Pôle Emploi: {str(e)}")
            # En cas d'erreur, utiliser les données fictives comme fallback
            return self._get_mock_data(keywords, location)
    
    def get_offer_details(self, offer_id: str) -> Dict[str, Any]:
        """
        Récupère les détails d'une offre d'emploi spécifique
        """
        try:
            response = requests.get(
                f"{self.BASE_URL}/offres/{offer_id}",
                headers=self._get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Erreur lors de la récupération des détails de l'offre {offer_id}: {str(e)}")
            return {}
    
    def map_to_offer_schema(self, pole_emploi_offer: Dict[str, Any]) -> OfferCreate:
        """
        Convertit une offre Pôle Emploi au format de notre application
        """
        # Extraction des technologies mentionnées dans l'offre
        tech_list = []
        if "competences" in pole_emploi_offer:
            for competence in pole_emploi_offer.get("competences", []):
                tech_name = competence.get("libelle", "").strip()
                if tech_name:
                    tech_list.append(TechCreate(
                        name=tech_name,
                        category="Compétence",
                        description=f"Compétence extraite de Pôle Emploi: {tech_name}"
                    ))
        
        # Extraction du salaire s'il est disponible
        salary_min = None
        salary_max = None
        if "salaire" in pole_emploi_offer and pole_emploi_offer["salaire"]:
            salary_info = pole_emploi_offer["salaire"]
            if "libelle" in salary_info and salary_info["libelle"]:
                # Tentative d'extraction des valeurs numériques du libellé
                salary_text = salary_info["libelle"]
                # Logique d'extraction à implémenter selon le format
        
        # Déterminer si le poste est en remote
        remote = False
        if "lieuTravail" in pole_emploi_offer:
            lieu_travail = pole_emploi_offer["lieuTravail"]
            if "libelle" in lieu_travail and "TELETRAVAIL" in lieu_travail["libelle"].upper():
                remote = True
        
        # Mapping des types de contrat
        contract_mapping = {
            "CDI": "CDI",
            "CDD": "CDD",
            "MIS": "Intérim",
            "SAI": "Saisonnier",
            "LIB": "Freelance"
        }
        
        contract_type = "Autre"
        if "typeContrat" in pole_emploi_offer:
            contract_code = pole_emploi_offer.get("typeContrat")
            contract_type = contract_mapping.get(contract_code, "Autre")
        
        # Création de l'objet OfferCreate
        return OfferCreate(
            title=pole_emploi_offer.get("intitule", "Sans titre"),
            company=pole_emploi_offer.get("entreprise", {}).get("nom", "Entreprise non précisée"),
            location=pole_emploi_offer.get("lieuTravail", {}).get("libelle", "Lieu non précisé"),
            description=pole_emploi_offer.get("description", ""),
            salary_min=salary_min,
            salary_max=salary_max,
            contract_type=contract_type,
            remote=remote,
            url=pole_emploi_offer.get("origineOffre", {}).get("urlOrigine", ""),
            posted_at=datetime.now(),  # À ajuster si la date est disponible dans l'API
            tech_ids=[],  # Sera rempli après création des technologies
            techs=tech_list
        )
