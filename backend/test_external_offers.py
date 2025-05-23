import requests
import json

# Test de l'endpoint /api/external-offers
print("=== Test de l'endpoint /api/external-offers ===")
response = requests.get("http://localhost:8082/api/external-offers?location=Bordeaux&sources=all&limit=5")

if response.status_code == 200:
    data = response.json()
    print(f"Statut: {response.status_code}")
    print(f"Nombre d'offres: {len(data)}")
    
    if len(data) > 0:
        for i, offer in enumerate(data[:2]):
            print(f"Offre {i+1}: {offer.get('title')} - {offer.get('location')}")
    else:
        print("Aucune offre trouvée.")
else:
    print(f"Erreur: {response.status_code}")
    print(response.text)
