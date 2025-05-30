import React from 'react';
import type { TechTrend } from '../types/tech';

interface TechTrendCardProps {
  trend: TechTrend;
  rank: number;
}

/**
 * Carte affichant une tendance technologique avec son rang et ses statistiques
 * Design moderne suivant les directives de style JobTech Radar
 */
const TechTrendCard: React.FC<TechTrendCardProps> = ({ trend, rank }) => {
  // Déterminer le style en fonction du rang
  const getStyles = () => {
    if (rank === 1) return {
      card: 'bg-gradient-to-br from-amber-50 to-amber-100 border-amber-400 shadow-amber-100/50',
      badge: 'bg-amber-500 text-white',
      progress: 'bg-amber-500'
    };
    if (rank === 2) return {
      card: 'bg-gradient-to-br from-gray-50 to-gray-100 border-gray-400 shadow-gray-100/50',
      badge: 'bg-gray-500 text-white',
      progress: 'bg-gray-500'
    };
    if (rank === 3) return {
      card: 'bg-gradient-to-br from-amber-50/80 to-amber-100/80 border-amber-300 shadow-amber-100/30',
      badge: 'bg-amber-400 text-white',
      progress: 'bg-amber-400'
    };
    return {
      card: 'bg-white border-indigo-100 shadow-indigo-100/30',
      badge: 'bg-indigo-600 text-white',
      progress: 'bg-indigo-600'
    };
  };

  const styles = getStyles();

  return (
    <div 
      className={`rounded-xl p-5 border ${styles.card} shadow-lg transition-all duration-300 hover:shadow-xl hover:translate-y-[-4px]`}
    >
      <div className="flex justify-between items-center mb-3">
        <h3 className="text-xl font-bold text-gray-800 flex items-center gap-2">
          {trend.name}
          {rank <= 3 && (
            <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-amber-100 text-amber-700 text-xs font-bold">
              {rank === 1 ? '🏆' : rank === 2 ? '🥈' : '🥉'}
            </span>
          )}
        </h3>
        <span className={`flex items-center justify-center h-8 min-w-8 rounded-full ${styles.badge} text-sm font-bold px-3`}>#{rank}</span>
      </div>
      
      <div className="mt-2">
        <span className="inline-block bg-gray-100 text-gray-800 rounded-full px-3 py-1 text-sm font-medium">
          {trend.category}
        </span>
      </div>
      
      <div className="mt-5">
        <div className="flex justify-between text-sm font-medium mb-2">
          <span className="text-gray-700">Popularité</span>
          <span className="text-indigo-700 font-bold">{trend.percentage.toFixed(1)}%</span>
        </div>
        <div className="w-full bg-gray-100 rounded-full h-3">
          <div
            className={`${styles.progress} h-3 rounded-full transition-all duration-500 ease-out`}
            style={{ width: `${trend.percentage}%` }}
          ></div>
        </div>
        <div className="mt-3 flex items-center justify-between">
          <p className="text-sm text-gray-600">
            <span className="font-bold text-gray-800">{trend.count}</span> offres
          </p>
          <span className="text-xs text-indigo-600 font-medium bg-indigo-50 px-2 py-1 rounded-md">
            {trend.percentage > 15 ? 'Très demandée' : trend.percentage > 10 ? 'Demandée' : 'Émergente'}
          </span>
        </div>
      </div>
    </div>
  );
};

export default TechTrendCard;
