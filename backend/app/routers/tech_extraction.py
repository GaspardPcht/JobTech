from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.database import get_db
from app.models import Offer, Tech
from app.schemas.tech import TechInDB
import re

router = APIRouter(
    prefix="/tech-extraction",
    tags=["tech-extraction"],
    responses={404: {"description": "Not found"}},
)

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

@router.get("/analyze-text", response_model=List[str])
async def analyze_text(text: str):
    """
    Analyse un texte et retourne les technologies détectées
    """
    return extract_technologies_from_text(text)

@router.post("/analyze-offer/{offer_id}", response_model=List[TechInDB])
async def analyze_offer(
    offer_id: int,
    db: Session = Depends(get_db)
):
    """
    Analyse une offre spécifique et retourne les technologies détectées
    """
    # Récupérer l'offre
    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offre non trouvée")
    
    # Analyser le titre et la description
    text_to_analyze = f"{offer.title} {offer.description or ''}"
    tech_names = extract_technologies_from_text(text_to_analyze)
    
    # Récupérer les technologies correspondantes en base de données
    techs = db.query(Tech).filter(Tech.name.in_(tech_names)).all()
    
    return techs

@router.post("/sync-all-offers", status_code=status.HTTP_202_ACCEPTED)
async def sync_all_offers(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Lance une tâche en arrière-plan pour synchroniser les technologies de toutes les offres
    """
    def sync_task():
        from app.services.tech_service import TechService
        from app.schemas.tech import TechCreate
        
        # Récupérer toutes les offres
        offers = db.query(Offer).all()
        
        for offer in offers:
            # Extraire les technologies du titre et de la description
            text_to_analyze = f"{offer.title} {offer.description or ''}"
            tech_names = extract_technologies_from_text(text_to_analyze)
            
            if tech_names:
                for tech_name in tech_names:
                    # Rechercher la technologie par son nom
                    db_tech = TechService.get_tech_by_name(db, tech_name)
                    
                    if not db_tech:
                        # Créer la technologie si elle n'existe pas
                        tech_create = TechCreate(
                            name=tech_name,
                            category="Technologie",
                            description=f"Technologie extraite automatiquement: {tech_name}"
                        )
                        db_tech = TechService.create_tech(db, tech_create)
                    
                    # Vérifier si la technologie est déjà associée à l'offre
                    if db_tech not in offer.techs:
                        offer.techs.append(db_tech)
                
                db.commit()
    
    background_tasks.add_task(sync_task)
    return {"message": "Synchronisation des technologies lancée en arrière-plan"}
