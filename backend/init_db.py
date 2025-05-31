#!/usr/bin/env python3
"""
Script pour initialiser la base de données.
Exécuter ce script avant de démarrer l'application pour la première fois.
"""
from app.init_db import init_db

if __name__ == "__main__":
    init_db()
