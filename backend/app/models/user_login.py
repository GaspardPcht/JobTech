from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class UserLogin(Base):
    """
    Modèle pour stocker les informations de connexion des utilisateurs
    """
    __tablename__ = "user_logins"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    login_time = Column(DateTime, default=datetime.utcnow)
    
    # Relation avec l'utilisateur
    user = relationship("User", back_populates="logins")
