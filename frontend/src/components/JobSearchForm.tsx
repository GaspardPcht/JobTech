import React, { useState } from 'react';
import type { OfferFilters } from '../types/offer';

interface JobSearchFormProps {
  onSearch: (filters: OfferFilters) => void;
  initialFilters?: OfferFilters;
}

const JobSearchForm: React.FC<JobSearchFormProps> = ({
  onSearch,
  initialFilters = {},
}) => {
  const [filters, setFilters] = useState<OfferFilters>({
    keywords: initialFilters.keywords || '',
    location: initialFilters.location || '',
    contract_type: initialFilters.contract_type || '',
    remote: initialFilters.remote || false,
    sources: initialFilters.sources || 'all',
    limit: initialFilters.limit || 50,
    tech_only: initialFilters.tech_only || false,
    sort_by: initialFilters.sort_by || 'date',
    page: initialFilters.page || 0,
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(filters);
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value, type } = e.target;

    if (type === 'checkbox') {
      setFilters({
        ...filters,
        [name]: (e.target as HTMLInputElement).checked,
      });
    } else {
      setFilters({
        ...filters,
        [name]: value,
      });
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white rounded-lg shadow-md p-6 mb-6"
    >
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
        <div>
          <label
            htmlFor="keywords"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Mots-clés
          </label>
          <input
            type="text"
            id="keywords"
            name="keywords"
            value={filters.keywords || ''}
            onChange={handleChange}
            placeholder="Ex: développeur, data scientist..."
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <div>
          <label
            htmlFor="location"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Localisation
          </label>
          <input
            type="text"
            id="location"
            name="location"
            value={filters.location || ''}
            onChange={handleChange}
            placeholder="Ex: Paris, Lyon, Bordeaux..."
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <div>
          <label
            htmlFor="contract_type"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Type de contrat
          </label>
          <select
            id="contract_type"
            name="contract_type"
            value={filters.contract_type || ''}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="">Tous les contrats</option>
            <option value="CDI">CDI</option>
            <option value="CDD">CDD</option>
            <option value="Freelance">Freelance</option>
            <option value="Stage">Stage</option>
            <option value="Alternance">Alternance</option>
          </select>
        </div>

        <div>
          <label
            htmlFor="sources"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Sources
          </label>
          <select
            id="sources"
            name="sources"
            value={filters.sources || 'all'}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="all">Toutes les sources</option>
            <option value="adzuna">Adzuna</option>
            <option value="pole-emploi">Pôle Emploi</option>
          </select>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div>
          <label
            htmlFor="sort_by"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Trier par
          </label>
          <select
            id="sort_by"
            name="sort_by"
            value={filters.sort_by || 'date'}
            onChange={handleChange}
            className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="date">Date (plus récent)</option>
            <option value="relevance">Pertinence</option>
          </select>
        </div>
      </div>

      <div className="flex items-center justify-between">
        <div className="flex items-center">
          <input
            type="checkbox"
            id="remote"
            name="remote"
            checked={filters.remote || false}
            onChange={handleChange}
            className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
          />
          <label htmlFor="remote" className="ml-2 block text-sm text-gray-700">
            Télétravail uniquement
          </label>
        </div>

        <button
          type="submit"
          className="bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded-md transition-colors duration-300"
        >
          Rechercher
        </button>
      </div>
    </form>
  );
};

export default JobSearchForm;
