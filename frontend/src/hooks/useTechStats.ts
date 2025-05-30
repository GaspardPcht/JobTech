import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getTechStats, getTechTrends, syncAllTechs } from '../services/techService';

/**
 * Hook pour récupérer les statistiques des technologies
 */
export const useTechStats = () => {
  return useQuery({
    queryKey: ['techStats'],
    queryFn: getTechStats,
  });
};

/**
 * Hook pour récupérer les tendances des technologies
 */
export const useTechTrends = (limit: number = 20) => {
  return useQuery({
    queryKey: ['techTrends', limit],
    queryFn: () => getTechTrends(limit),
  });
};

/**
 * Hook pour synchroniser les technologies de toutes les offres
 */
export const useSyncTechs = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: syncAllTechs,
    onSuccess: () => {
      // Invalider les requêtes pour forcer un rechargement des données
      queryClient.invalidateQueries({ queryKey: ['techStats'] });
      queryClient.invalidateQueries({ queryKey: ['techTrends'] });
    },
  });
};
