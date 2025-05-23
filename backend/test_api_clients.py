from app.integrations.adzuna import AdzunaClient
from app.integrations.pole_emploi import PoleEmploiClient

# Test du client Adzuna
print("=== Test du client Adzuna ===")
adzuna_client = AdzunaClient()
adzuna_response = adzuna_client.search_offers(location="Bordeaux")
print(f"Nombre d'offres Adzuna: {len(adzuna_response.get('results', []))}")
for i, offer in enumerate(adzuna_response.get('results', [])[:2]):
    print(f"Offre {i+1}: {offer.get('title')} - {offer.get('location', {}).get('display_name')}")

# Test du client Pôle Emploi
print("\n=== Test du client Pôle Emploi ===")
pole_emploi_client = PoleEmploiClient()
pole_emploi_response = pole_emploi_client.search_offers(location="Bordeaux")
print(f"Nombre d'offres Pôle Emploi: {len(pole_emploi_response.get('resultats', []))}")
for i, offer in enumerate(pole_emploi_response.get('resultats', [])[:2]):
    print(f"Offre {i+1}: {offer.get('intitule')} - {offer.get('lieuTravail', {}).get('libelle')}")
