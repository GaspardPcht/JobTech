import sys
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Tech, Offer, offer_tech
from app.schemas.tech import TechCreate
from app.services.tech_service import TechService
import logging
import re

# Configuration du logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_technologies_from_text(text: str) -> list:
    """
    Extrait les technologies mentionnées dans un texte
    en utilisant une liste prédéfinie de technologies courantes
    """
    if not text:
        return []
        
    common_techs = [
        "Python", "JavaScript", "TypeScript", "Java", "C#", "C++", "PHP", "Ruby",
        "Swift", "Kotlin", "Go", "Rust", "React", "Angular", "Vue", "Node.js",
        "Django", "Flask", "Spring", "ASP.NET", "Laravel", "Ruby on Rails",
        "SQL", "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch",
        "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Git", "CI/CD",
        "TensorFlow", "PyTorch", "Pandas", "NumPy", "Scikit-learn",
        # Ajout de technologies supplémentaires
        "HTML", "CSS", "SASS", "LESS", "Bootstrap", "Tailwind", "Material UI",
        "GraphQL", "REST", "API", "Microservices", "DevOps", "Agile", "Scrum",
        "Jenkins", "Travis CI", "CircleCI", "GitHub Actions", "GitLab CI",
        "Linux", "Unix", "Windows", "MacOS", "Android", "iOS", "Mobile",
        "Frontend", "Backend", "Fullstack", "Web", "Mobile", "Desktop",
        "Machine Learning", "Deep Learning", "AI", "Artificial Intelligence",
        "Data Science", "Big Data", "Data Engineering", "ETL", "Data Warehouse",
        "Business Intelligence", "Power BI", "Tableau", "Looker", "Metabase",
        "Cybersecurity", "Security", "Cryptography", "Blockchain", "Smart Contract"
    ]
    
    found_techs = []
    for tech in common_techs:
        # Recherche du mot entier avec une regex
        pattern = r'\b' + re.escape(tech) + r'\b'
        if re.search(pattern, text, re.IGNORECASE):
            found_techs.append(tech)
    
    return found_techs

def get_or_create_tech(db: Session, tech_name: str) -> Tech:
    """
    Récupère une technologie par son nom ou la crée si elle n'existe pas
    """
    # Rechercher la technologie par son nom (insensible à la casse)
    db_tech = TechService.get_tech_by_name(db, tech_name)
    
    if not db_tech:
        # Créer la technologie si elle n'existe pas
        tech_create = TechCreate(
            name=tech_name,
            category="Technologie",
            description=f"Technologie extraite automatiquement: {tech_name}"
        )
        db_tech = TechService.create_tech(db, tech_create)
        logger.info(f"Nouvelle technologie créée: {tech_name}")
    
    return db_tech

def sync_technologies():
    """
    Synchronise les technologies pour toutes les offres en base de données
    """
    db = SessionLocal()
    try:
        # Récupérer toutes les offres
        offers = db.query(Offer).all()
        logger.info(f"Nombre total d'offres: {len(offers)}")
        
        # Compteurs pour les statistiques
        total_techs_added = 0
        offers_updated = 0
        
        for offer in offers:
            # Extraire les technologies du titre et de la description
            text_to_analyze = f"{offer.title} {offer.description or ''}"
            tech_names = extract_technologies_from_text(text_to_analyze)
            
            if tech_names:
                # Récupérer ou créer les technologies
                techs_added = 0
                for tech_name in tech_names:
                    db_tech = get_or_create_tech(db, tech_name)
                    
                    # Vérifier si la technologie est déjà associée à l'offre
                    if db_tech not in offer.techs:
                        offer.techs.append(db_tech)
                        techs_added += 1
                
                if techs_added > 0:
                    logger.info(f"Offre {offer.id} ({offer.title}): {techs_added} technologies ajoutées")
                    total_techs_added += techs_added
                    offers_updated += 1
                    db.commit()
        
        logger.info(f"Synchronisation terminée: {total_techs_added} technologies ajoutées à {offers_updated} offres")
    
    except Exception as e:
        db.rollback()
        logger.error(f"Erreur lors de la synchronisation des technologies: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    # Demander confirmation
    confirm = input("Voulez-vous synchroniser les technologies pour toutes les offres ? (o/n): ")
    
    if confirm.lower() == 'o':
        sync_technologies()
    else:
        print("Opération annulée.")
        sys.exit(0)
