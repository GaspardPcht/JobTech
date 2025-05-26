from datetime import timedelta
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserCreate, Token
from app.utils.security import (
    verify_password, 
    get_password_hash, 
    create_access_token, 
    ACCESS_TOKEN_EXPIRE_MINUTES
)


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Récupère un utilisateur par son email
    """
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """
    Récupère un utilisateur par son nom d'utilisateur
    """
    return db.query(User).filter(User.username == username).first()


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Authentifie un utilisateur avec son email et son mot de passe
    """
    user = get_user_by_email(db, email)
    
    if not user:
        return None
    
    if not verify_password(password, user.hashed_password):
        return None
    
    return user


def create_user(db: Session, user_create: UserCreate) -> User:
    """
    Crée un nouvel utilisateur
    """
    try:
        print(f"Tentative de création d'utilisateur avec: {user_create.dict()}")
        
        # Vérifie si l'email existe déjà
        existing_email = get_user_by_email(db, user_create.email)
        if existing_email:
            print(f"Email déjà utilisé: {user_create.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cet email est déjà utilisé"
            )
        
        # Vérifie si le nom d'utilisateur existe déjà
        existing_username = get_user_by_username(db, user_create.username)
        if existing_username:
            print(f"Nom d'utilisateur déjà utilisé: {user_create.username}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ce nom d'utilisateur est déjà utilisé"
            )
        
        # Crée l'utilisateur avec le mot de passe haché
        hashed_password = get_password_hash(user_create.password)
        db_user = User(
            email=user_create.email,
            username=user_create.username,
            hashed_password=hashed_password
        )
        
        # Ajoute l'utilisateur à la base de données
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        print(f"Utilisateur créé avec succès: {db_user.email}")
        return db_user
    except Exception as e:
        print(f"Erreur lors de la création de l'utilisateur: {str(e)}")
        raise


def login_user(db: Session, email: str, password: str) -> Token:
    """
    Connecte un utilisateur et génère un token JWT
    """
    user = authenticate_user(db, email, password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crée un token JWT avec une durée d'expiration
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")
