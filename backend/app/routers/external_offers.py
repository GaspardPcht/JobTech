from fastapi import APIRouter, BackgroundTasks, HTTPException, Query, status
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

# Configuration du logger
logger = logging.getLogger(__name__)

from app.integrations.adzuna import AdzunaClient
from app.integrations.pole_emploi import PoleEmploiClient
from app.schemas.offer import OfferResponse

router = APIRouter(
    prefix="/external-offers",
    tags=["external-offers"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[OfferResponse])
async def search_external_offers(
    keywords: Optional[str] = None,
    location: Optional[str] = None,
    contract_type: Optional[str] = None,
    remote: Optional[bool] = None,
    sources: Optional[str] = "all",  # "all", "adzuna", "pole-emploi"
    sort_by: Optional[str] = "date",  # "date", "relevance"
    limit: int = 50,
    page: int = 0,
    tech_only: bool = True  # Toujours activé par défaut car JobTech est dédié aux offres tech
):
    # Log des paramètres reçus
    logger.info(f"Paramètres reçus: keywords={keywords}, location={location}, tech_only={tech_only}, page={page}")
    """
    Recherche des offres d'emploi directement auprès des API externes (Pôle Emploi, Adzuna)
    sans les stocker dans la base de données locale.
    """
    results = []
    
    # Déterminer quelles sources utiliser
    use_adzuna = sources.lower() in ["all", "adzuna"]
    use_pole_emploi = sources.lower() in ["all", "pole-emploi"]
    
    # Recherche sur Adzuna
    if use_adzuna:
        try:
            adzuna_client = AdzunaClient()
            adzuna_response = adzuna_client.search_offers(
                keywords=keywords,
                location=location,
                page=page + 1,  # Adzuna commence à la page 1
                per_page=limit
            )
            
            # Convertir les offres Adzuna en schéma OfferResponse
            for offer_data in adzuna_response.get("results", []):
                offer_schema = adzuna_client.map_to_offer_schema(offer_data)
                
                # Filtrer par type de contrat si spécifié
                if contract_type and offer_schema.contract_type != contract_type:
                    continue
                
                # Filtrer par remote si spécifié
                if remote is not None and offer_schema.remote != remote:
                    continue
                
                # Convertir en OfferResponse
                offer_response = OfferResponse(
                    id=0,  # ID fictif car non stocké en base
                    title=offer_schema.title,
                    company=offer_schema.company,
                    location=offer_schema.location,
                    description=offer_schema.description,
                    salary_min=offer_schema.salary_min,
                    salary_max=offer_schema.salary_max,
                    contract_type=offer_schema.contract_type,
                    remote=offer_schema.remote,
                    url=offer_schema.url,
                    posted_at=datetime.now(),  # Utiliser la date actuelle car posted_at n'existe pas dans OfferCreate
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    techs=[tech for tech in offer_schema.techs] if hasattr(offer_schema, 'techs') else []
                )
                
                results.append(offer_response)
        except Exception as e:
            print(f"Erreur lors de la recherche sur Adzuna: {str(e)}")
    
    # Recherche sur Pôle Emploi
    if use_pole_emploi:
        try:
            pole_emploi_client = PoleEmploiClient()
            pole_emploi_offers = pole_emploi_client.search_offers(
                keywords=keywords,
                location=location,
                page=page,  # Pôle Emploi commence à la page 0
                per_page=limit
            )
            
            # Convertir les offres Pôle Emploi en schéma OfferResponse
            for offer_data in pole_emploi_offers:
                offer_schema = pole_emploi_client.map_to_offer_schema(offer_data)
                
                # Filtrer par type de contrat si spécifié
                if contract_type and offer_schema.contract_type != contract_type:
                    continue
                
                # Filtrer par remote si spécifié
                if remote is not None and offer_schema.remote != remote:
                    continue
                
                # Convertir en OfferResponse
                offer_response = OfferResponse(
                    id=0,  # ID fictif car non stocké en base
                    title=offer_schema.title,
                    company=offer_schema.company,
                    location=offer_schema.location,
                    description=offer_schema.description,
                    salary_min=offer_schema.salary_min,
                    salary_max=offer_schema.salary_max,
                    contract_type=offer_schema.contract_type,
                    remote=offer_schema.remote,
                    url=offer_schema.url,
                    posted_at=datetime.now(),  # Utiliser la date actuelle car posted_at n'existe pas dans OfferCreate
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    techs=[tech for tech in offer_schema.techs] if hasattr(offer_schema, 'techs') else []
                )
                
                results.append(offer_response)
        except Exception as e:
            print(f"Erreur lors de la recherche sur Pôle Emploi: {str(e)}")
    
    # Filtrer les offres tech si demandé
    logger.info(f"Nombre d'offres avant filtrage tech: {len(results)}")
    if tech_only:
        logger.info("Filtrage des offres tech activé")
        
        # Liste des mots-clés qui définissent clairement une offre tech
        tech_keywords = [
            # Développement
            "développeur", "developer", "software", "web", "frontend", "backend", "fullstack", "code", "coding", "programmeur", "programmer",
            
            # Langages de programmation
            "python", "javascript", "typescript", "java", "c#", "c++", "php", "ruby", "go", "rust", "scala", "kotlin", "swift", "perl", "r",
            
            # Frameworks et librairies
            "react", "angular", "vue", "node", "django", "flask", "spring", "asp.net", "laravel", "symfony", "express", ".net", "rails",
            
            # Data science et IA
            "data scientist", "data engineer", "machine learning", "deep learning", "intelligence artificielle", "artificial intelligence", "ia", "ai", "nlp", "computer vision",
            
            # DevOps et Cloud
            "devops", "cloud", "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "terraform", "ansible", "ci/cd", "gitlab", "github",
            
            # Mobile
            "mobile", "android", "ios", "swift", "kotlin", "flutter", "react native", "xamarin", "cordova", "ionic",
            
            # Bases de données
            "database", "sql", "nosql", "mongodb", "postgresql", "mysql", "oracle", "cassandra", "redis", "elasticsearch",
            
            # Sécurité et réseaux
            "cybersecurity", "security", "réseau", "network", "système", "system", "pentester", "ethical hacker", "firewall", "vpn",
            
            # Technologies émergentes
            "blockchain", "crypto", "iot", "internet of things", "objets connectés", "ar", "vr", "realité augmentée", "realité virtuelle",
            
            # Rôles techniques
            "ingénieur", "engineer", "architect", "architecte", "tech", "informatique", "it", "cto", "cio", "technical", "technique",
            
            # Data et analytics
            "data", "données", "analytics", "analyse", "bi", "business intelligence", "data mining", "big data", "hadoop", "spark",
            
            # Méthodologies et outils
            "agile", "scrum", "kanban", "jira", "git", "github", "gitlab", "bitbucket", "versionning", "versioning",
            
            # QA et tests
            "qa", "quality assurance", "test", "testing", "testeur", "tester", "automation", "selenium", "cypress", "junit", "jest",
            
            # Design et UX
            "ux", "ui", "user experience", "user interface", "design", "graphiste", "figma", "sketch", "adobe xd",
            
            # Web marketing technique
            "seo", "sem", "référencement", "webmaster", "webdesigner", "growth hacker", "growth hacking"
        ]
        
        # Mots-clés à exclure (métiers non-tech qui peuvent contenir des mots-clés tech)
        exclude_keywords = [
            "paysagiste", "jardinier", "agricole", "agriculture", "fleuriste", "boulanger", "boucher", "cuisinier", "chef", "serveur", 
            "barman", "hôtesse", "receptionniste", "ménage", "nettoyage", "entretien", "mécanicien", "plombier", "chauffeur", "livreur",
            "commercial", "vendeur", "vente", "retail", "magasin", "boutique", "caissier", "secrétaire", "assistant", "administratif",
            "comptable", "finance", "juridique", "avocat", "notaire", "médecin", "infirmier", "santé", "pharmacien", "dentiste",
            "enseignant", "professeur", "formateur", "animateur", "coach", "sport", "fitness", "bien-être", "esthéticien", "coiffeur",
            "architecte d'intérieur", "décorateur", "immobilier", "agent immobilier", "courtier", "assurance", "banque", "conseiller",
            "ressources humaines", "recruteur", "rh", "communication", "marketing", "journaliste", "rédacteur", "traducteur", "interprète"
        ]
        
        # Fonction pour vérifier si une offre est tech
        def is_tech_offer(offer):
            # D'abord vérifier si l'offre contient des mots-clés à exclure
            title_lower = offer.title.lower()
            description_lower = offer.description.lower() if offer.description else ""
            
            # Liste de mots-clés qui indiquent clairement que l'offre n'est PAS tech
            non_tech_jobs = [
                "receptionniste", "paysagiste", "jardinier", "agricole", "agriculture", "fleuriste", 
                "boulanger", "boucher", "cuisinier", "chef", "serveur", "barman", "hôtesse", 
                "ménage", "nettoyage", "entretien", "mécanicien", "plombier", "chauffeur", "livreur",
                "commercial", "vendeur", "vente", "retail", "magasin", "boutique", "caissier", 
                "secrétaire", "assistant", "administratif", "comptable", "finance", "juridique", 
                "avocat", "notaire", "médecin", "infirmier", "santé", "pharmacien", "dentiste",
                "enseignant", "professeur", "formateur", "animateur", "coach", "sport", "fitness", 
                "bien-être", "esthéticien", "coiffeur", "architecte d'intérieur", "décorateur", 
                "immobilier", "agent immobilier", "courtier", "assurance", "banque", "conseiller",
                "ressources humaines", "recruteur", "rh", "communication", "marketing", "journaliste", 
                "rédacteur", "traducteur", "interprète"
            ]
            
            # Vérifier si le titre contient explicitement un métier non-tech
            for job in non_tech_jobs:
                if job in title_lower:
                    logger.info(f"Offre explicitement non-tech (titre): {offer.title} - Métier non-tech: {job}")
                    return False
            
            # Vérifier les mots-clés d'exclusion dans le titre
            for keyword in exclude_keywords:
                if keyword.lower() in title_lower:
                    logger.info(f"Offre exclue (titre contient mot-clé non-tech): {offer.title} - Mot-clé d'exclusion: {keyword}")
                    return False
            
            # Rechercher des mots-clés tech dans le titre
            title_has_tech = False
            for keyword in tech_keywords:
                if keyword.lower() in title_lower:
                    logger.info(f"Offre tech trouvée (titre): {offer.title} - Mot-clé: {keyword}")
                    title_has_tech = True
                    break
            
            # Si le titre contient un mot-clé tech, c'est une offre tech
            if title_has_tech:
                return True
            
            # Vérifier si la description contient explicitement un métier non-tech
            if description_lower:
                for job in non_tech_jobs:
                    if job in description_lower:
                        logger.info(f"Offre explicitement non-tech (description): {offer.title} - Métier non-tech: {job}")
                        return False
                
                # Vérifier les mots-clés d'exclusion dans la description
                for keyword in exclude_keywords:
                    if keyword.lower() in description_lower:
                        logger.info(f"Offre exclue (description contient mot-clé non-tech): {offer.title} - Mot-clé d'exclusion: {keyword}")
                        return False
                
                # Rechercher des mots-clés tech dans la description
                # Compter combien de mots-clés tech sont présents dans la description
                tech_keyword_count = 0
                matched_keywords = []
                
                for keyword in tech_keywords:
                    if keyword.lower() in description_lower:
                        tech_keyword_count += 1
                        matched_keywords.append(keyword)
                        # Si on trouve au moins 2 mots-clés tech, c'est une offre tech
                        if tech_keyword_count >= 2:
                            logger.info(f"Offre tech trouvée (description contient plusieurs mots-clés tech): {offer.title} - Mots-clés: {matched_keywords}")
                            return True
            
            # Vérifier dans les technologies associées
            if hasattr(offer, 'techs') and offer.techs:
                logger.info(f"Offre tech trouvée (technologies): {offer.title} - Techs: {offer.techs}")
                return True
            
            # Si on a trouvé exactement 1 mot-clé tech dans la description, vérifier s'il s'agit d'un mot-clé fort
            if description_lower and tech_keyword_count == 1:
                strong_tech_keywords = [
                    "développeur", "developer", "software", "python", "javascript", "java", "c#", "c++",
                    "react", "angular", "vue", "node", "django", "flask", "spring", "data scientist",
                    "devops", "cloud", "aws", "azure", "cybersecurity", "fullstack", "backend", "frontend",
                    "mobile", "android", "ios", "machine learning", "intelligence artificielle"
                ]
                
                for keyword in strong_tech_keywords:
                    if keyword.lower() in description_lower:
                        logger.info(f"Offre tech trouvée (description contient un mot-clé tech fort): {offer.title} - Mot-clé: {keyword}")
                        return True
            
            # Pas une offre tech
            logger.info(f"Offre non-tech: {offer.title}")
            return False
        
        # Filtrer les offres tech
        filtered_results = [offer for offer in results if is_tech_offer(offer)]
        logger.info(f"Nombre d'offres après filtrage tech: {len(filtered_results)} (sur {len(results)} offres au total)")
        results = filtered_results
    
    # Trier les résultats si demandé
    if sort_by == "date":
        # Trier par date de publication (la plus récente en premier)
        results.sort(key=lambda x: x.posted_at, reverse=True)
    
    # Limiter le nombre de résultats
    return results[:limit]
