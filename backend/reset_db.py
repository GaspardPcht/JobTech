import os
import sys
from sqlalchemy import create_engine
from app.database import Base, engine
from app.models import *  # Importer tous les modèles pour qu'ils soient enregistrés dans Base.metadata

def reset_database():
    """
    Supprime la base de données existante et la recrée avec les tables vides
    """
    # Chemin vers le fichier de base de données
    db_path = "./jobtech.db"
    
    # Vérifier si le fichier existe
    if os.path.exists(db_path):
        print(f"Suppression de la base de données existante: {db_path}")
        os.remove(db_path)
        print("Base de données supprimée avec succès.")
    else:
        print("Aucune base de données existante trouvée.")
    
    # Recréer les tables
    print("Création des nouvelles tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables créées avec succès.")
    
    print("Réinitialisation de la base de données terminée.")

if __name__ == "__main__":
    # Demander confirmation
    confirm = input("Êtes-vous sûr de vouloir réinitialiser la base de données ? Toutes les données seront perdues. (o/n): ")
    
    if confirm.lower() == 'o':
        reset_database()
    else:
        print("Opération annulée.")
        sys.exit(0)
