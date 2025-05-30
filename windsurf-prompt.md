JobTech Radar — Prompt Guide pour Windsurf

🎯 Vision du projet

JobTech Radar est une application web moderne qui aide les développeurs et étudiants tech à :

	•	Trouver des offres d’emploi pertinentes
	•	Identifier les technologies les plus demandées
	•	Organiser leurs candidatures
	•	Centraliser leur veille tech

L’objectif est de créer une plateforme élégante, rapide, modulaire, et professionnelle, en suivant les meilleures pratiques d’architecture frontend/backend utilisées en entreprise.

⸻

🧱 Architecture technique

🧭 Choix généraux
	•	Frontend : React + TypeScript avec Vite (rapide, moderne)
	•	Backend : FastAPI (Python 3.11+)
	•	Base de données : PostgreSQL
	•	Visualisation : Recharts ou Chart.js
	•	API REST : backend exposé via /api/...


📁 Arborescence React (Vite + TS)
frontend/
├── public/
├── src/
│   ├── assets/              # Images, logos, icônes
│   ├── components/          # Composants réutilisables (Header, Button, Card, etc.)
│   ├── features/            # Domaines fonctionnels (Offers, TechTrends, Candidatures)
│   ├── hooks/               # Hooks custom
│   ├── lib/                 # Fonctions utilitaires (formatting, validation, etc.)
│   ├── pages/               # Pages entières (accueil, dashboard, etc.)
│   ├── services/            # Appels API (via axios ou react-query)
│   ├── styles/              # Tailwind config ou CSS globaux
│   ├── types/               # Types et interfaces TypeScript
│   ├── App.tsx
│   └── main.tsx

🎨 Design & UI

Couleurs modernes, élégantes :
	•	Couleur primaire : #6366F1 (Indigo)
	•	Accent : #10B981 (Emerald / Success)
	•	Background clair : #F9FAFB
	•	Texte principal : #111827
	•	Texte secondaire : #6B7280
	•	Danger : #EF4444

Framework UI :
	•	Tailwind CSS avec design inspiré de shadcn/ui
→ boutons, cards, inputs, modaux sobres et modernes

⸻

✅ Conventions frontend
	•	Utiliser TypeScript partout (props, API, composants)
	•	Nommer les composants en PascalCase
	•	Utiliser useEffect proprement avec cleanup si nécessaire
	•	Jamais de any en TypeScript
	•	Utiliser react-query ou axios pour appels API (centralisés dans services/)
	•	Gestion de l’état local : useState, useReducer, ou Zustand (pas Redux sauf besoin complexe)
	•	Pas de code mort ni console.log en prod
	•	Linting et Prettier actifs

⸻

⚙️ Backend (FastAPI)
	•	Structure modulaire avec dossiers :
	•	routers/, models/, schemas/, services/, utils/
	•	Utiliser Pydantic pour les schémas
	•	Routes RESTful (/api/offers, /api/techs, /api/candidatures)
	•	Stockage dans PostgreSQL via SQLAlchemy
	•	Connexion à la DB via database.py centralisé
	•	Tests : pytest

⸻

🚀 Déploiement & outils
	•	Docker : un conteneur pour le backend, un pour le frontend, un pour PostgreSQL
	•	Dockerfile et docker-compose.yml à jour
	•	GitHub Actions pour lint + test (bonus)

⸻

🧪 Règles Windsurf (à respecter strictement)
	•	💬 Toujours commenter les fonctions publiques
	•	📦 Respecter l’arborescence définie
	•	📐 Proposer des composants réutilisables dès que possible
	•	🧼 Ne jamais mélanger logique métier et affichage
	•	✅ Fournir des props typées (pas de any)
	•	🧠 Ne pas proposer de refacto non demandé
	•	🧱 Ne pas créer de nouvelles structures sans validation
	•	🔁 Utiliser des fonctions ou hooks existants si déjà présents
	•	❌ Ne jamais utiliser localStorage ou window dans la logique métier (passer par des hooks)