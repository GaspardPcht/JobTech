import axios from 'axios';
import type { Offer, OfferFilters } from '../types/offer';

const API_URL = 'http://localhost:8082/api';

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
