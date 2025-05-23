from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Récupérer l'URL de la base de données depuis les variables d'environnement
# Utiliser SQLite par défaut pour faciliter le développement
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./jobtech.db")

# Créer le moteur SQLAlchemy
# Pour SQLite, il est important d'activer le support des clés étrangères
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# Créer une session locale
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Créer une classe de base pour les modèles
Base = declarative_base()

# Fonction pour obtenir une session de base de données
def get_db():
    """
    Crée une nouvelle session de base de données pour chaque requête
    et la ferme à la fin de la requête
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
