import os
import shutil

# Chemin du fichier à modifier
file_path = "/Users/gaspard/Desktop/PROJETS/JobTech/backend/app/routers/external_offers.py"

# Lire le contenu du fichier
with open(file_path, 'r') as file:
    content = file.read()

# Remplacer la ligne problématique pour les offres Pôle Emploi
# Nous cherchons spécifiquement la deuxième occurrence qui est dans le bloc Pôle Emploi
# Nous utilisons un remplacement avec contexte pour être sûr de cibler la bonne partie
old_text = """                # Convertir en OfferResponse
                offer_response = OfferResponse(
                    id=offer_schema.id,  # ID fictif car non stocké en base
                    title=offer_schema.title,"""

new_text = """                # Convertir en OfferResponse
                offer_response = OfferResponse(
                    id=0,  # ID fictif car non stocké en base (OfferCreate n'a pas d'attribut id)
                    title=offer_schema.title,"""

# Trouver la deuxième occurrence
first_pos = content.find(old_text)
if first_pos != -1:
    # Chercher la deuxième occurrence après la première
    second_pos = content.find(old_text, first_pos + 1)
    if second_pos != -1:
        # Remplacer seulement la deuxième occurrence
        content = content[:second_pos] + new_text + content[second_pos + len(old_text):]
        
        # Sauvegarder le fichier modifié
        with open(file_path, 'w') as file:
            file.write(content)
        
        print("Fichier modifié avec succès!")
    else:
        print("Deuxième occurrence non trouvée.")
else:
    print("Première occurrence non trouvée.")

print("Script terminé.")
