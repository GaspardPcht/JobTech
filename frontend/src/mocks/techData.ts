import type { TechWithStats, TechTrend } from '../types/tech';

// Données de test pour les statistiques des technologies
export const mockTechStats: TechWithStats[] = [
  { id: 1, name: 'JavaScript', category: 'Langage', description: 'Langage de programmation pour le web', offer_count: 120 },
  { id: 2, name: 'React', category: 'Framework', description: 'Bibliothèque JavaScript pour créer des interfaces utilisateur', offer_count: 95 },
  { id: 3, name: 'Python', category: 'Langage', description: 'Langage de programmation polyvalent', offer_count: 85 },
  { id: 4, name: 'Node.js', category: 'Runtime', description: 'Environnement d\'exécution JavaScript côté serveur', offer_count: 78 },
  { id: 5, name: 'TypeScript', category: 'Langage', description: 'Superset typé de JavaScript', offer_count: 65 },
  { id: 6, name: 'Angular', category: 'Framework', description: 'Framework pour applications web', offer_count: 60 },
  { id: 7, name: 'Vue.js', category: 'Framework', description: 'Framework JavaScript progressif', offer_count: 55 },
  { id: 8, name: 'Java', category: 'Langage', description: 'Langage de programmation orienté objet', offer_count: 50 },
  { id: 9, name: 'Docker', category: 'DevOps', description: 'Plateforme de conteneurisation', offer_count: 45 },
  { id: 10, name: 'Kubernetes', category: 'DevOps', description: 'Système d\'orchestration de conteneurs', offer_count: 40 },
];

// Données de test pour les tendances des technologies
export const mockTechTrends: TechTrend[] = [
  { name: 'JavaScript', category: 'Langage', count: 120, percentage: 24 },
  { name: 'React', category: 'Framework', count: 95, percentage: 19 },
  { name: 'Python', category: 'Langage', count: 85, percentage: 17 },
  { name: 'Node.js', category: 'Runtime', count: 78, percentage: 15.6 },
  { name: 'TypeScript', category: 'Langage', count: 65, percentage: 13 },
  { name: 'Angular', category: 'Framework', count: 60, percentage: 12 },
  { name: 'Vue.js', category: 'Framework', count: 55, percentage: 11 },
  { name: 'Java', category: 'Langage', count: 50, percentage: 10 },
  { name: 'Docker', category: 'DevOps', count: 45, percentage: 9 },
  { name: 'Kubernetes', category: 'DevOps', count: 40, percentage: 8 },
];
