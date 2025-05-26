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
    
    # La méthode _get_mock_data a été supprimée car nous utilisons maintenant l'API réelle
    
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
            # Limiter le nombre d'offres par page à 50 maximum (limitation de l'API Pôle Emploi)
            limited_per_page = min(per_page, 50)
            
            # Préparer les paramètres de recherche
            params = {
                "range": f"{page * limited_per_page}-{(page + 1) * limited_per_page - 1}",  # Format: "0-19", "20-39", etc.
                "sort": 1  # Tri par date de création décroissante
            }
            
            # Codes ROME spécifiques aux métiers tech
            tech_rome_codes = [
                "M1801",  # Administration de systèmes d'information
                "M1802",  # Expertise et support en systèmes d'information
                "M1803",  # Direction des systèmes d'information
                "M1804",  # Etudes et développement de réseaux de télécommunications
                "M1805",  # Etudes et développement informatique
                "M1806",  # Conseil et maîtrise d'ouvrage en systèmes d'information
                "M1810",  # Production et exploitation de systèmes d'information
                "E1101",  # Animation de site multimédia
                "E1104",  # Conception de contenus multimédia
                "E1205",  # Réalisation de contenus multimédia
                "H1202",  # Conception et dessin de produits électriques et électroniques
                "H1208",  # Intervention technique en études et conception en automatisme
                "H1209",  # Intervention technique en études et développement électronique
                "H1206"   # Management et ingénierie études, recherche et développement industriel
            ]
            
            # Ajouter les codes ROME spécifiques aux métiers tech
            params["codeROME"] = ",".join(tech_rome_codes)
            
            # Ajouter les paramètres optionnels s'ils sont fournis
            if keywords:
                params["motsCles"] = keywords
                
            if location:
                if location.isdigit() and len(location) == 5:
                    # C'est un code INSEE
                    params["commune"] = location
                elif len(location) == 2 and location.isdigit():
                    # C'est un code de département
                    params["departement"] = location
                else:
                    # C'est un nom de ville, l'ajouter aux mots-clés
                    if params["motsCles"]:
                        params["motsCles"] += f" {location}"
                    else:
                        params["motsCles"] = location
            
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
