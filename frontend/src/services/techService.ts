import axios from 'axios';
import type { TechWithStats, TechTrend } from '../types/tech';

const API_URL = 'http://localhost:8000/api';

/**
 * Récupère les statistiques des technologies (nombre d'offres par technologie)
 */
export const getTechStats = async (): Promise<TechWithStats[]> => {
  try {
    const response = await axios.get(`${API_URL}/techs/stats`);
    return response.data;
  } catch (error) {
    console.error('Erreur lors de la récupération des statistiques des technologies:', error);
    throw error;
  }
};

/**
 * Récupère les tendances des technologies (les plus demandées)
 */
export const getTechTrends = async (limit: number = 20): Promise<TechTrend[]> => {
  try {
    const response = await axios.get(`${API_URL}/techs/trends?limit=${limit}`);
    return response.data;
  } catch (error) {
    console.error('Erreur lors de la récupération des tendances technologiques:', error);
    throw error;
  }
};

/**
 * Lance la synchronisation des technologies pour toutes les offres
 */
export const syncAllTechs = async (): Promise<void> => {
  try {
    await axios.post(`${API_URL}/tech-extraction/sync-all-offers`);
  } catch (error) {
    console.error('Erreur lors de la synchronisation des technologies:', error);
    throw error;
  }
};
