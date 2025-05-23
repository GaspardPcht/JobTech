# JobTech Radar - Frontend

## 🎯 Description

JobTech Radar est une plateforme moderne qui permet aux développeurs et étudiants de trouver des offres d'emploi pertinentes, analyser les technologies les plus demandées, suivre leurs candidatures et centraliser leur veille tech.

## 🛠️ Technologies

- React 18+
- TypeScript
- Vite
- Tailwind CSS

## 📁 Structure du projet

```
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
```

## 🚀 Installation et démarrage

```bash
# Installation des dépendances
npm install

# Démarrage du serveur de développement
npm run dev

# Construction pour la production
npm run build
```

## 🎨 Design System

Couleurs principales :
- Couleur primaire : `#6366F1` (Indigo)
- Accent : `#10B981` (Emerald / Success)
- Background clair : `#F9FAFB`
- Texte principal : `#111827`
- Texte secondaire : `#6B7280`
- Danger : `#EF4444`

## 📝 Conventions

- TypeScript partout (pas de `any`)
- Composants en PascalCase
- Gestion propre des effets avec cleanup
- Appels API centralisés dans `services/`
