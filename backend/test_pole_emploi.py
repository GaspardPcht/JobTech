from app.integrations.pole_emploi import PoleEmploiClient
import logging

# Configurer le logging pour voir les messages de débogage
logging.basicConfig(level=logging.INFO)

# Test du client Pôle Emploi
print("=== Test du client Pôle Emploi ===")
pole_emploi_client = PoleEmploiClient()

# Tester l'authentification
try:
    pole_emploi_client._authenticate()
    print(f"Authentification réussie: {pole_emploi_client.access_token is not None}")
except Exception as e:
    print(f"Erreur d'authentification: {str(e)}")

# Tester la recherche d'offres
try:
    pole_emploi_response = pole_emploi_client.search_offers(location="33063", distance=10)  # Code INSEE de Bordeaux
    print(f"Nombre d'offres Pôle Emploi: {len(pole_emploi_response.get('resultats', []))}")
    
    # Afficher les premières offres
    for i, offer in enumerate(pole_emploi_response.get('resultats', [])[:2]):
        print(f"Offre {i+1}: {offer.get('intitule')} - {offer.get('lieuTravail', {}).get('libelle')}")
except Exception as e:
    print(f"Erreur lors de la recherche d'offres: {str(e)}")
