import requests
import json

# Test de l'endpoint /api/external-offers avec suivi des redirections
print("=== Test de l'endpoint /api/external-offers avec suivi des redirections ===")

# Paramètres de la requête
params = {
    "keywords": "data",
    "location": "bordeaux",
    "sources": "all",
    "limit": 20
}

# URL de l'API
url = "http://localhost:8082/api/external-offers"

# Effectuer la requête sans suivre les redirections
print(f"Requête: GET {url} avec params={params}")
response_no_redirect = requests.get(url, params=params, allow_redirects=False)
print(f"Sans redirection - Status code: {response_no_redirect.status_code}")
print(f"Sans redirection - Headers: {dict(response_no_redirect.headers)}")

# Effectuer la requête en suivant les redirections
print("\nMaintenant avec redirection:")
response_with_redirect = requests.get(url, params=params, allow_redirects=True)
print(f"Avec redirection - Status code: {response_with_redirect.status_code}")
print(f"Avec redirection - URL finale: {response_with_redirect.url}")

# Traiter la réponse
if response_with_redirect.status_code == 200:
    try:
        data = response_with_redirect.json()
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
        print(f"Contenu: {response_with_redirect.text[:500]}...")
else:
    print(f"Erreur: {response_with_redirect.status_code}")
    print(f"Contenu: {response_with_redirect.text[:500]}...")
