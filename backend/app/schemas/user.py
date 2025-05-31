from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Union
from datetime import datetime


class UserBase(BaseModel):
    """Schéma de base pour les utilisateurs"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)


class UserCreate(UserBase):
    """Schéma pour la création d'un utilisateur"""
    password: str = Field(..., min_length=8)
    
    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "username",
                "password": "password123"
            }
        }


class UserLogin(BaseModel):
    """Schéma pour la connexion d'un utilisateur"""
    email: EmailStr
    password: str


class UserResponse(UserBase):
    """Schéma pour la réponse après création/récupération d'un utilisateur"""
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
        orm_mode = True  # Pour la compatibilité avec les anciennes versions de Pydantic


class UserRegisterResponse(UserResponse):
    """Schéma pour la réponse après inscription d'un utilisateur, incluant un token"""
    access_token: str
    token_type: str


class Token(BaseModel):
    """Schéma pour le token d'authentification"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schéma pour les données contenues dans le token"""
    email: Optional[str] = None
    exp: Optional[Union[datetime, str]] = None
    role: Optional[str] = "user"  # Par défaut, tous les utilisateurs ont le rôle 'user'
