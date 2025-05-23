import { useQuery } from '@tanstack/react-query';
import { getExternalOffers } from '../services/offerService';
import type { Offer, OfferFilters } from '../types/offer';

/**
 * Hook pour récupérer les offres d'emploi en temps réel
 * @param filters Filtres à appliquer à la recherche
 * @returns Résultat de la requête (données, statut de chargement, erreur)
 */
export const useExternalOffers = (filters: OfferFilters = {}) => {
  return useQuery<Offer[], Error>({
    queryKey: ['externalOffers', filters],
    queryFn: () => getExternalOffers(filters),
    staleTime: 5 * 60 * 1000, 
    refetchOnWindowFocus: false,
  });
};
