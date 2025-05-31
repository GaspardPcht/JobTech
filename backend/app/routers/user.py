from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, Token, UserRegisterResponse
from app.services.auth_service import create_user, login_user
from app.utils.security import get_current_active_user
from app.models.user import User

# Créez le routeur
router = APIRouter(prefix="/api/auth", tags=["auth"])

# Route d'inscription
@router.post("/register", response_model=UserRegisterResponse, status_code=status.HTTP_201_CREATED)
def register(user_create: UserCreate, db: Session = Depends(get_db)):
    """
    Inscription d'un nouvel utilisateur et génération d'un token JWT
    """
    try:
        print(f"Données reçues pour l'inscription: {user_create.dict()}")
        
        user, access_token = create_user(db, user_create)
        # Retourner l'utilisateur avec le token JWT
        return UserRegisterResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            is_active=user.is_active,
            created_at=user.created_at,
            access_token=access_token,
            token_type="bearer"
        )
    except Exception as e:
        print(f"Erreur lors de l'inscription: {str(e)}")
        raise

# Route de connexion
@router.post("/login", response_model=Token)
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Connexion d'un utilisateur existant
    Enregistre également les informations de connexion (IP, user-agent)
    """
    # Récupérer l'adresse IP et l'user-agent
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    
    print(f"Tentative de connexion depuis IP: {ip_address}, User-Agent: {user_agent}")
    
    # OAuth2PasswordRequestForm utilise username comme champ, mais nous utilisons email pour l'authentification
    return login_user(db, form_data.username, form_data.password, ip_address, user_agent)

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