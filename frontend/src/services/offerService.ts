import axios from 'axios';
import type { Offer, OfferFilters } from '../types/offer';

// Utiliser l'URL de l'API depuis le fichier .env
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

/**
 * Récupère les offres d'emploi en temps réel depuis les API externes
 * @param filters Filtres à appliquer à la recherche
 * @returns Liste des offres d'emploi
 */
export const getExternalOffers = async (filters: OfferFilters = {}): Promise<Offer[]> => {
  const response = await axios.get(`${API_URL}/external-offers/`, { 
    params: filters 
  });
  return response.data;
};

/**
 * Filtre les offres pour ne garder que celles liées à la tech
 * @param offers Liste des offres à filtrer
 * @returns Liste des offres filtrées
 */
export const filterTechOffers = (offers: Offer[]): Offer[] => {
  const techKeywords = [
    'développeur', 'developer', 'software', 'web', 'frontend', 'backend', 'fullstack',
    'python', 'javascript', 'java', 'c#', 'c++', 'php', 'ruby', 'go', 'rust',
    'react', 'angular', 'vue', 'node', 'django', 'flask', 'spring',
    'data scientist', 'machine learning', 'devops', 'cloud', 'aws', 'azure',
    'mobile', 'android', 'ios', 'database', 'sql', 'nosql', 'mongodb',
    'cybersecurity', 'security', 'réseau', 'network', 'système',
    'ingénieur', 'engineer', 'architect', 'architecte', 'tech', 'informatique',
    'data', 'analytics', 'intelligence artificielle', 'ia', 'ai'
  ];
  
  const nonTechJobs = [
    'receptionniste', 'paysagiste', 'jardinier', 'agricole', 'fleuriste', 'boulanger',
    'chef', 'serveur', 'barman', 'hôtesse', 'ménage', 'nettoyage', 'plombier',
    'chauffeur', 'livreur', 'vendeur', 'vente', 'magasin', 'boutique', 'caissier'
  ];
  
  return offers.filter(offer => {
    const title = offer.title.toLowerCase();
    const description = offer.description ? offer.description.toLowerCase() : '';
    
    // Exclure les offres avec des métiers non-tech dans le titre
    for (const job of nonTechJobs) {
      if (title.includes(job)) {
        return false;
      }
    }
    
    // Inclure les offres avec des mots-clés tech dans le titre
    for (const keyword of techKeywords) {
      if (title.includes(keyword)) {
        return true;
      }
    }
    
    // Inclure les offres avec des mots-clés tech dans la description
    for (const keyword of techKeywords) {
      if (description.includes(keyword)) {
        return true;
      }
    }
    
    // Par défaut, exclure l'offre
    return false;
  });
};

/**
 * Formate le salaire pour l'affichage
 * @param min Salaire minimum
 * @param max Salaire maximum
 * @returns Chaîne formatée du salaire
 */
export const formatSalary = (min: number | null, max: number | null): string => {
  if (!min && !max) return 'Non précisé';
  if (min && !max) return `${min.toLocaleString('fr-FR')}€`;
  if (!min && max) return `Jusqu'à ${max.toLocaleString('fr-FR')}€`;
  return `${min?.toLocaleString('fr-FR')}€ - ${max?.toLocaleString('fr-FR')}€`;
};

/**
 * Formate le type de contrat pour l'affichage
 * @param contractType Type de contrat
 * @returns Chaîne formatée du type de contrat
 */
export const formatContractType = (contractType: string | null): string => {
  if (!contractType) return 'Non précisé';
  
  const contractTypes: Record<string, string> = {
    'CDI': 'CDI',
    'CDD': 'CDD',
    'Freelance': 'Freelance',
    'Stage': 'Stage',
    'Alternance': 'Alternance',
    'Intérim': 'Intérim',
    'Autre': 'Autre'
  };
  
  return contractTypes[contractType] || contractType;
};