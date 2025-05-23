import requests
import json
from pprint import pprint

# Test de l'endpoint /api/external-offers avec plus de détails
print("=== Test détaillé de l'endpoint /api/external-offers ===")

# Paramètres de la requête
params = {
    "location": "Bordeaux",
    "sources": "all",  # "all", "adzuna", "pole-emploi"
    "limit": 10
}

# URL de l'API
url = "http://localhost:8082/api/external-offers"

# Effectuer la requête
print(f"Requête: GET {url} avec params={params}")
response = requests.get(url, params=params)

# Afficher les informations de la réponse
print(f"Status code: {response.status_code}")
print(f"Headers: {dict(response.headers)}")
print(f"URL finale: {response.url}")

# Traiter la réponse
if response.status_code == 200:
    try:
        data = response.json()
        print(f"Nombre d'offres: {len(data)}")
        
        if len(data) > 0:
            print("\nDétails des premières offres:")
            for i, offer in enumerate(data[:3]):
                print(f"\nOffre {i+1}:")
                print(f"  Titre: {offer.get('title')}")
                print(f"  Entreprise: {offer.get('company')}")
                print(f"  Lieu: {offer.get('location')}")
                print(f"  Type de contrat: {offer.get('contract_type')}")
                print(f"  URL: {offer.get('url')}")
        else:
            print("Aucune offre trouvée.")
    except json.JSONDecodeError:
        print("Erreur: La réponse n'est pas au format JSON")
        print(f"Contenu: {response.text[:500]}...")
else:
    print(f"Erreur: {response.status_code}")
    print(f"Contenu: {response.text[:500]}...")
