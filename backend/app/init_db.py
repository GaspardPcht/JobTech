from app.database import engine, Base
from app.models.user import User
# Import d'autres modèles
from app.models.user_login import UserLogin

def init_db():
    """
    Initialise la base de données en créant toutes les tables définies dans les modèles
    """
    print("Création des tables dans la base de données...")
    Base.metadata.create_all(bind=engine)
    print("Tables créées avec succès!")

if __name__ == "__main__":
    init_db()
