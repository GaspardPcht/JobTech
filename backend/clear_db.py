import sys
from sqlalchemy import create_engine, inspect, MetaData, Table
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal
from app.models import *  # Importer tous les modèles pour qu'ils soient enregistrés dans Base.metadata

def clear_all_tables():
    """
    Vide toutes les tables de la base de données sans supprimer la structure
    """
    db = SessionLocal()
    inspector = inspect(engine)
    metadata = MetaData()
    
    try:
        # Désactiver temporairement les contraintes de clés étrangères pour SQLite
        db.execute("PRAGMA foreign_keys = OFF")
        
        # Obtenir tous les noms de tables
        table_names = inspector.get_table_names()
        print(f"Tables trouvées: {table_names}")
        
        # Supprimer les données de chaque table
        for table_name in table_names:
            print(f"Vidage de la table: {table_name}")
            # Utiliser l'API SQLAlchemy Core pour les opérations de suppression
            table = Table(table_name, metadata, autoload_with=engine)
            db.execute(table.delete())
        
        # Réactiver les contraintes de clés étrangères
        db.execute("PRAGMA foreign_keys = ON")
        
        # Valider les changements
        db.commit()
        print("Toutes les tables ont été vidées avec succès.")
        
    except Exception as e:
        db.rollback()
        print(f"Erreur lors du vidage des tables: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    # Demander confirmation
    confirm = input("Êtes-vous sûr de vouloir vider toutes les tables de la base de données ? Toutes les données seront perdues. (o/n): ")
    
    if confirm.lower() == 'o':
        clear_all_tables()
    else:
        print("Opération annulée.")
        sys.exit(0)
