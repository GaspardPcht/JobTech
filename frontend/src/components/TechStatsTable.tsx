import React, { useState } from 'react';
import type { TechWithStats } from '../types/tech';

interface TechStatsTableProps {
  techs: TechWithStats[];
  isLoading: boolean;
}

const TechStatsTable: React.FC<TechStatsTableProps> = ({ techs, isLoading }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState<'name' | 'category' | 'offer_count'>('offer_count');
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('desc');

  // Filtrer les technologies en fonction du terme de recherche
  const filteredTechs = techs.filter(
    (tech) =>
      tech.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      tech.category.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Trier les technologies
  const sortedTechs = [...filteredTechs].sort((a, b) => {
    if (sortBy === 'name') {
      return sortDirection === 'asc'
        ? a.name.localeCompare(b.name)
        : b.name.localeCompare(a.name);
    }
    if (sortBy === 'category') {
      return sortDirection === 'asc'
        ? a.category.localeCompare(b.category)
        : b.category.localeCompare(a.category);
    }
    // Par défaut, trier par nombre d'offres
    return sortDirection === 'asc'
      ? a.offer_count - b.offer_count
      : b.offer_count - a.offer_count;
  });

  // Gérer le changement de colonne de tri
  const handleSort = (column: 'name' | 'category' | 'offer_count') => {
    if (sortBy === column) {
      // Inverser la direction si on clique sur la même colonne
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      // Nouvelle colonne, trier par défaut en ordre décroissant
      setSortBy(column);
      setSortDirection('desc');
    }
  };

  // Obtenir l'icône de tri pour une colonne
  const getSortIcon = (column: 'name' | 'category' | 'offer_count') => {
    if (sortBy !== column) return null;
    return sortDirection === 'asc' ? '↑' : '↓';
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="overflow-x-auto">
      <div className="mb-4">
        <input
          type="text"
          placeholder="Rechercher une technologie..."
          className="w-full p-2 border border-gray-300 rounded-md"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>
      <table className="min-w-full bg-white">
        <thead className="bg-gray-100">
          <tr>
            <th
              className="py-3 px-4 text-left cursor-pointer hover:bg-gray-200"
              onClick={() => handleSort('name')}
            >
              Nom {getSortIcon('name')}
            </th>
            <th
              className="py-3 px-4 text-left cursor-pointer hover:bg-gray-200"
              onClick={() => handleSort('category')}
            >
              Catégorie {getSortIcon('category')}
            </th>
            <th
              className="py-3 px-4 text-left cursor-pointer hover:bg-gray-200"
              onClick={() => handleSort('offer_count')}
            >
              Nombre d'offres {getSortIcon('offer_count')}
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {sortedTechs.map((tech) => (
            <tr key={tech.id} className="hover:bg-gray-50">
              <td className="py-2 px-4">{tech.name}</td>
              <td className="py-2 px-4">
                <span className="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700">
                  {tech.category}
                </span>
              </td>
              <td className="py-2 px-4 font-semibold">{tech.offer_count}</td>
            </tr>
          ))}
          {sortedTechs.length === 0 && (
            <tr>
              <td colSpan={3} className="py-4 text-center text-gray-500">
                Aucune technologie trouvée
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default TechStatsTable;
