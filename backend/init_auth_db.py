"""
Script pour initialiser la base de données avec les tables d'authentification
"""
from app.database import engine, Base
from app.models.user import User  # Importe le modèle User pour créer la table
from app.utils.security import get_password_hash

# Créer les tables
Base.metadata.create_all(bind=engine)

print("Tables d'authentification créées avec succès !")

# Vous pouvez également créer un utilisateur de test si nécessaire
from sqlalchemy.orm import Session
from app.database import SessionLocal

db = SessionLocal()
try:
    # Vérifier si un utilisateur de test existe déjà
    test_user = db.query(User).filter(User.email == "test@example.com").first()
    
    if not test_user:
        # Créer un utilisateur de test
        test_user = User(
            email="test@example.com",
            username="testuser",
            hashed_password=get_password_hash("password123"),
            is_active=True
        )
        db.add(test_user)
        db.commit()
        print("Utilisateur de test créé avec succès !")
    else:
        print("L'utilisateur de test existe déjà.")
finally:
    db.close()
