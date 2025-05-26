from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, Token
from app.services.auth_service import create_user, login_user
from app.utils.security import get_current_active_user
from app.models.user import User

# Créez le routeur
router = APIRouter(prefix="/api/auth", tags=["auth"])

# Route d'inscription
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_create: UserCreate, db: Session = Depends(get_db)):
    """
    Inscription d'un nouvel utilisateur
    """
    try:
        print(f"Données reçues pour l'inscription: {user_create.dict()}")
        
        user = create_user(db, user_create)
        # Convertir explicitement l'objet SQLAlchemy en dictionnaire pour Pydantic
        return UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            is_active=user.is_active,
            created_at=user.created_at
        )
    except Exception as e:
        print(f"Erreur lors de l'inscription: {str(e)}")
        raise

# Route de connexion
@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Connexion d'un utilisateur existant
    """
    # OAuth2PasswordRequestForm utilise username comme champ, mais nous utilisons email pour l'authentification
    return login_user(db, form_data.username, form_data.password)

# Route pour obtenir l'utilisateur actuel
@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_active_user)):
    """
    Récupère les informations de l'utilisateur connecté
    """
    # Convertir explicitement l'objet SQLAlchemy en dictionnaire pour Pydantic
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        is_active=current_user.is_active,
        created_at=current_user.created_at
    )