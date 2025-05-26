from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random

from app.database import SessionLocal, engine, Base
from app.models import Offer, Tech, Candidature, CandidatureStatus
from app.models.user import User
from app.utils.security import get_password_hash

def init_db():
    """
    Initialise la base de données avec des données de test
    """
    # Création des tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Vérifier si des données existent déjà
    if db.query(Tech).count() > 0:
        print("La base de données contient déjà des données. Initialisation annulée.")
        db.close()
        return
    
    # Création des technologies
    technologies = [
        # Frontend
        Tech(name="React", category="Frontend", description="Bibliothèque JavaScript pour construire des interfaces utilisateur"),
        Tech(name="Angular", category="Frontend", description="Framework JavaScript pour construire des applications web"),
        Tech(name="Vue.js", category="Frontend", description="Framework JavaScript progressif pour construire des interfaces utilisateur"),
        Tech(name="TypeScript", category="Frontend", description="Sur-ensemble typé de JavaScript"),
        Tech(name="Tailwind CSS", category="Frontend", description="Framework CSS utilitaire"),
        Tech(name="Next.js", category="Frontend", description="Framework React pour le rendu côté serveur"),
        
        # Backend
        Tech(name="Node.js", category="Backend", description="Environnement d'exécution JavaScript côté serveur"),
        Tech(name="Python", category="Backend", description="Langage de programmation interprété"),
        Tech(name="Java", category="Backend", description="Langage de programmation orienté objet"),
        Tech(name="C#", category="Backend", description="Langage de programmation orienté objet"),
        Tech(name="Go", category="Backend", description="Langage de programmation compilé"),
        Tech(name="Ruby", category="Backend", description="Langage de programmation interprété"),
        Tech(name="PHP", category="Backend", description="Langage de script côté serveur"),
        Tech(name="FastAPI", category="Backend", description="Framework web moderne pour Python"),
        Tech(name="Django", category="Backend", description="Framework web pour Python"),
        Tech(name="Spring Boot", category="Backend", description="Framework pour Java"),
        Tech(name="Express.js", category="Backend", description="Framework web pour Node.js"),
        Tech(name="ASP.NET Core", category="Backend", description="Framework web pour .NET"),
        
        # Database
        Tech(name="PostgreSQL", category="Database", description="Système de gestion de base de données relationnelle"),
        Tech(name="MySQL", category="Database", description="Système de gestion de base de données relationnelle"),
        Tech(name="MongoDB", category="Database", description="Base de données NoSQL orientée documents"),
        Tech(name="Redis", category="Database", description="Magasin de structure de données en mémoire"),
        Tech(name="SQLite", category="Database", description="Bibliothèque de base de données SQL légère"),
        
        # DevOps
        Tech(name="Docker", category="DevOps", description="Plateforme de conteneurisation"),
        Tech(name="Kubernetes", category="DevOps", description="Système d'orchestration de conteneurs"),
        Tech(name="AWS", category="DevOps", description="Services cloud d'Amazon"),
        Tech(name="Azure", category="DevOps", description="Services cloud de Microsoft"),
        Tech(name="Google Cloud", category="DevOps", description="Services cloud de Google"),
        Tech(name="Jenkins", category="DevOps", description="Serveur d'automatisation"),
        Tech(name="GitLab CI/CD", category="DevOps", description="Intégration continue et déploiement continu"),
        Tech(name="GitHub Actions", category="DevOps", description="Automatisation des workflows GitHub"),
    ]
    
    db.add_all(technologies)
    db.commit()
    
    # Récupérer les technologies créées
    techs = db.query(Tech).all()
    
    # Création des offres d'emploi
    companies = [
        "Google", "Microsoft", "Amazon", "Apple", "Facebook", "Netflix", "Spotify",
        "Twitter", "Airbnb", "Uber", "Lyft", "Slack", "Dropbox", "Pinterest", "Shopify",
        "Atlassian", "Twilio", "Stripe", "Square", "Zoom"
    ]
    
    locations = [
        "Paris", "Lyon", "Marseille", "Bordeaux", "Lille", "Toulouse", "Nantes",
        "Strasbourg", "Montpellier", "Rennes", "Remote", "Hybrid"
    ]
    
    contract_types = ["CDI", "CDD", "Freelance", "Stage", "Alternance"]
    
    job_titles = [
        "Développeur Frontend", "Développeur Backend", "Développeur Fullstack",
        "Ingénieur DevOps", "Architecte Logiciel", "Data Scientist",
        "Ingénieur Machine Learning", "Développeur Mobile", "UX/UI Designer",
        "Product Manager", "Scrum Master", "Tech Lead", "CTO"
    ]
    
    offers = []
    for i in range(50):
        # Sélectionner des technologies aléatoires pour cette offre
        offer_techs = random.sample(techs, random.randint(3, 8))
        
        # Créer l'offre
        offer = Offer(
            title=f"{random.choice(job_titles)} - {random.choice(['Junior', 'Senior', 'Mid-level'])}",
            company=random.choice(companies),
            location=random.choice(locations),
            description=f"Description de l'offre d'emploi {i+1}. Nous recherchons un développeur talentueux pour rejoindre notre équipe.",
            salary_min=random.randint(30, 60) * 1000,
            salary_max=random.randint(60, 120) * 1000,
            contract_type=random.choice(contract_types),
            remote=random.choice([True, False]),
            url=f"https://example.com/jobs/{i+1}",
            posted_at=datetime.utcnow() - timedelta(days=random.randint(0, 30)),
            techs=offer_techs
        )
        offers.append(offer)
    
    db.add_all(offers)
    db.commit()
    
    # Récupérer les offres créées
    db_offers = db.query(Offer).all()
    
    # Création des candidatures
    candidatures = []
    for i in range(20):
        # Sélectionner une offre aléatoire
        offer = random.choice(db_offers)
        
        # Créer la candidature
        status = random.choice(list(CandidatureStatus))
        application_date = datetime.utcnow() - timedelta(days=random.randint(0, 15))
        
        candidature = Candidature(
            offer_id=offer.id,
            status=status,
            application_date=application_date,
            notes=f"Notes pour la candidature {i+1}",
            next_step="Entretien technique" if status == CandidatureStatus.APPLIED else None,
            next_step_date=application_date + timedelta(days=random.randint(3, 10)) if status == CandidatureStatus.APPLIED else None
        )
        candidatures.append(candidature)
    
    db.add_all(candidatures)
    db.commit()
    
    # Création d'un utilisateur de test
    if db.query(User).count() == 0:
        test_user = User(
            email="test@example.com",
            username="testuser",
            hashed_password=get_password_hash("password123"),
            is_active=True
        )
        db.add(test_user)
        db.commit()
        print("Utilisateur de test créé avec succès !")
    
    db.close()
    print("Base de données initialisée avec succès !")

if __name__ == "__main__":
    init_db()
