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
    
    BASE_URL = "https://api.pole-emploi.io/partenaire/offresdemploi/v2"
    AUTH_URL = "https://entreprise.pole-emploi.fr/connexion/oauth2/access_token?realm=/partenaire"
    
    def _get_mock_data(self, keywords: Optional[str] = None, location: Optional[str] = None) -> Dict[str, Any]:
        """
        Génère des données fictives pour le développement
        """
        # Données fictives plus complètes pour simuler les vraies offres de Pôle Emploi
        mock_results = [
            {
                "id": "101",
                "intitule": "Ingénieur DevOps - France Travail",
                "description": "Nous recherchons un ingénieur DevOps pour notre équipe technique. Vous serez responsable de la mise en place et de la maintenance de notre infrastructure cloud, ainsi que de l'automatisation des processus de déploiement. Compétences requises: Docker, Kubernetes, AWS, CI/CD, Git.",
                "entreprise": {"nom": "CloudTech Solutions"},
                "lieuTravail": {"libelle": location or "Bordeaux"},
                "typeContrat": "CDI",
                "salaire": {"libelle": "45000 - 60000 EUR par an"},
                "dateCreation": "2025-05-20T10:00:00Z",
                "origineOffre": {"urlOrigine": "https://francetravail.io/offres/101"},
                "competences": [
                    {"libelle": "Docker"},
                    {"libelle": "Kubernetes"},
                    {"libelle": "AWS"},
                    {"libelle": "CI/CD"},
                    {"libelle": "Git"}
                ]
            },
            {
                "id": "102",
                "intitule": "Développeur Full Stack JavaScript - France Travail",
                "description": "Développeur Full Stack pour application web innovante dans le secteur de la fintech. Vous participerez au développement de nouvelles fonctionnalités et à l'amélioration de l'expérience utilisateur. Compétences requises: JavaScript, Node.js, React, MongoDB, Express.",
                "entreprise": {"nom": "WebSolutions Innovantes"},
                "lieuTravail": {"libelle": location or "Bordeaux"},
                "typeContrat": "CDI",
                "salaire": {"libelle": "40000 - 55000 EUR par an"},
                "dateCreation": "2025-05-21T14:30:00Z",
                "origineOffre": {"urlOrigine": "https://francetravail.io/offres/102"},
                "competences": [
                    {"libelle": "JavaScript"},
                    {"libelle": "Node.js"},
                    {"libelle": "React"},
                    {"libelle": "MongoDB"},
                    {"libelle": "Express"}
                ]
            },
            {
                "id": "103",
                "intitule": "Data Scientist Senior - France Travail",
                "description": "Data Scientist expérimenté pour analyse de données complexes et création de modèles prédictifs dans le secteur de la santé. Vous travaillerez sur des projets innovants utilisant l'intelligence artificielle pour améliorer les diagnostics médicaux. Compétences requises: Python, TensorFlow, PyTorch, SQL, Machine Learning.",
                "entreprise": {"nom": "DataInsight Health"},
                "lieuTravail": {"libelle": location or "Bordeaux"},
                "typeContrat": "CDI",
                "salaire": {"libelle": "50000 - 65000 EUR par an"},
                "dateCreation": "2025-05-22T09:15:00Z",
                "origineOffre": {"urlOrigine": "https://francetravail.io/offres/103"},
                "competences": [
                    {"libelle": "Python"},
                    {"libelle": "TensorFlow"},
                    {"libelle": "PyTorch"},
                    {"libelle": "SQL"},
                    {"libelle": "Machine Learning"}
                ]
            },
            {
                "id": "104",
                "intitule": "Architecte Cloud - France Travail",
                "description": "Architecte Cloud pour concevoir et mettre en œuvre des solutions d'infrastructure cloud scalables et sécurisées. Vous serez responsable de la conception de l'architecture technique et de la sélection des technologies appropriées. Compétences requises: AWS, Azure, GCP, Terraform, CloudFormation.",
                "entreprise": {"nom": "CloudArch Systems"},
                "lieuTravail": {"libelle": location or "Bordeaux"},
                "typeContrat": "CDI",
                "salaire": {"libelle": "55000 - 70000 EUR par an"},
                "dateCreation": "2025-05-19T11:45:00Z",
                "origineOffre": {"urlOrigine": "https://francetravail.io/offres/104"},
                "competences": [
                    {"libelle": "AWS"},
                    {"libelle": "Azure"},
                    {"libelle": "GCP"},
                    {"libelle": "Terraform"},
                    {"libelle": "CloudFormation"}
                ]
            },
            {
                "id": "105",
                "intitule": "Développeur Mobile React Native - France Travail",
                "description": "Développeur Mobile pour application cross-platform utilisant React Native. Vous serez responsable du développement et de la maintenance d'applications mobiles pour iOS et Android. Compétences requises: React Native, JavaScript, TypeScript, Redux, Git.",
                "entreprise": {"nom": "MobileApp Creators"},
                "lieuTravail": {"libelle": location or "Bordeaux"},
                "typeContrat": "CDI",
                "salaire": {"libelle": "40000 - 55000 EUR par an"},
                "dateCreation": "2025-05-18T15:30:00Z",
                "origineOffre": {"urlOrigine": "https://francetravail.io/offres/105"},
                "competences": [
                    {"libelle": "React Native"},
                    {"libelle": "JavaScript"},
                    {"libelle": "TypeScript"},
                    {"libelle": "Redux"},
                    {"libelle": "Git"}
                ]
            }
        ]
        
        # Filtrer par mots-clés si spécifiés
        if keywords:
            keywords_lower = keywords.lower()
            filtered_results = []
            for offer in mock_results:
                # Vérifier si les mots-clés sont dans le titre, la description ou les compétences
                if keywords_lower in offer["intitule"].lower() or \
                   keywords_lower in offer["description"].lower() or \
                   any(keywords_lower in comp["libelle"].lower() for comp in offer["competences"]):
                    filtered_results.append(offer)
            mock_results = filtered_results
        
        # Ajouter une indication que ce sont des données fictives dans le titre
        for offer in mock_results:
            if " - France Travail" not in offer["intitule"]:
                offer["intitule"] += " - France Travail"
        
        return {"resultats": mock_results}
    
    def __init__(self):
        """
        Initialise le client Pôle Emploi avec les identifiants d'API
        """
        # Utiliser les nouveaux identifiants fournis
        self.client_id = "PAR_jobtech_947f4c9cd50410535e838ae71660ad338f8823f417dbebee48ba0a6533952e44"
        self.client_secret = "5176b13fe02d3f0952d72824ee7081b88b976af5789a518d8de91dbe65babbaa"
        self.access_token = None
        self.token_expiry = datetime.now()
        
        logger.info(f"Initialisation du client Pôle Emploi avec ID: {self.client_id[:10]}...")
    
    def _authenticate(self) -> None:
        """
        Obtient un token d'accès pour l'API Pôle Emploi (France Travail)
        """
        if self.access_token and self.token_expiry > datetime.now():
            return
            
        try:
            # Vérifier que les identifiants sont configurés
            if not self.client_id or not self.client_secret:
                logger.error("Les identifiants API Pôle Emploi ne sont pas configurés correctement")
                raise ValueError("Les identifiants API Pôle Emploi ne sont pas configurés correctement")
            
            # Utiliser la méthode d'authentification qui fonctionne dans l'autre projet
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            # Utiliser exactement le même format de données que dans l'exemple qui fonctionne
            data = {
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'scope': 'api_offresdemploiv2 o2dsoffre'  # Utiliser les mêmes scopes que dans l'exemple
            }
            
            # Afficher les données pour le débogage
            logger.info(f"Tentative d'authentification Pôle Emploi avec la méthode qui fonctionne: URL={self.AUTH_URL}")
            
            response = requests.post(
                self.AUTH_URL,
                headers=headers,
                data=data
            )
            
            # Afficher la réponse pour le débogage
            logger.info(f"Réponse d'authentification Pôle Emploi: Status={response.status_code}, URL={response.url}")
            
            if response.status_code != 200:
                # Afficher le contenu de la réponse pour comprendre l'erreur
                logger.error(f"Contenu de la réponse d'erreur: {response.text}")
            
            response.raise_for_status()
            
            data = response.json()
            self.access_token = data.get("access_token")
            expires_in = data.get("expires_in", 3600)  # Par défaut 1 heure
            self.token_expiry = datetime.now() + timedelta(seconds=expires_in)
            
            logger.info("Authentification à l'API Pôle Emploi réussie")
        except requests.RequestException as e:
            logger.error(f"Erreur lors de l'authentification à l'API Pôle Emploi: {str(e)}")
            # En cas d'erreur d'authentification, pas de token
            self.access_token = None
    
    def _get_headers(self) -> Dict[str, str]:
        """
        Récupère les en-têtes pour les requêtes à l'API Pôle Emploi
        """
        try:
            self._authenticate()
            if self.access_token:
                return {
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
            else:
                # Retourner des en-têtes vides, ce qui forcera l'utilisation des données fictives
                return {}
        except Exception as e:
            logger.error(f"Impossible de récupérer les en-têtes d'authentification: {str(e)}")
            # Retourner des en-têtes vides, ce qui forcera l'utilisation des données fictives
            return {}

    def search_offers(self, keywords: Optional[str] = None, location: Optional[str] = None, distance: int = 10, contract_type: Optional[str] = None, page: int = 0, per_page: int = 20) -> List[Dict[str, Any]]:
        """
        Recherche des offres d'emploi dans l'API Pôle Emploi
        Format de l'API: GET /v2/offres/search
        """
        # Vérifier si l'authentification est valide
        if not self.access_token:
            self._authenticate()
            if not self.access_token:
                logger.warning("Pas de token d'accès valide, aucune offre ne sera retournée")
                return []

        try:
            # Construire les paramètres de recherche comme dans l'exemple qui fonctionne
            params = {
                "motsCles": keywords,
                "commune": location,
                "distance": distance,
                "typeContrat": contract_type,
                "range": f"{page * per_page}-{(page + 1) * per_page - 1}"
            }
            
            # Supprimer les paramètres None
            params = {k: v for k, v in params.items() if v is not None}
            
            # Ajouter le tri par pertinence
            params["sort"] = 1  # 1 = tri par pertinence
            
            # Afficher les paramètres pour le débogage
            logger.info(f"Requête Pôle Emploi: URL={self.BASE_URL}/offres/search, Params={params}")
            
            # Faire la requête GET comme dans l'exemple qui fonctionne
            response = requests.get(
                f"{self.BASE_URL}/offres/search",
                headers=self._get_headers(),
                params=params
            )
            
            # Afficher la réponse pour le débogage
            logger.info(f"Réponse Pôle Emploi: Status={response.status_code}")
            
            response.raise_for_status()
            
            data = response.json()
            # La réponse peut être directement une liste ou un dictionnaire avec une clé "resultats"
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                return data.get("resultats", [])
            else:
                logger.warning(f"Format de réponse inattendu: {type(data)}")
                return []
        except requests.RequestException as e:
            logger.error(f"Erreur lors de la recherche d'offres Pôle Emploi: {str(e)}")
            # En cas d'erreur, retourner une liste vide
            return []
    
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
