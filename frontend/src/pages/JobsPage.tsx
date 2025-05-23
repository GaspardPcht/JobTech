import React, { useState } from 'react';
import JobCard from '../components/JobCard';
import JobSearchForm from '../components/JobSearchForm';
import { useExternalOffers } from '../hooks/useExternalOffers';
import type { OfferFilters } from '../types/offer';

const JobsPage: React.FC = () => {
  const [filters, setFilters] = useState<OfferFilters>({
    keywords: '',
    location: '',
    sources: 'all',
    limit: 50,
    sort_by: 'date' // Tri par date par défaut (plus récent en premier)
  });

  const { data: offers, isLoading, error, refetch } = useExternalOffers(filters);

  const handleSearch = (newFilters: OfferFilters) => {
    setFilters(newFilters);
    refetch();
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-indigo-600 mb-6">Offres d'emploi</h1>
      <p className="text-gray-600 mb-8">
        Découvrez les dernières offres d'emploi dans le domaine de la tech, mises à jour en temps réel depuis Adzuna et Pôle Emploi.
      </p>
      
      <JobSearchForm onSearch={handleSearch} initialFilters={filters} />
      
      {isLoading && (
        <div className="flex justify-center items-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-600"></div>
        </div>
      )}
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6" role="alert">
          <p className="font-bold">Erreur</p>
          <p>{error.message}</p>
        </div>
      )}
      
      {!isLoading && !error && offers && offers.length === 0 && (
        <div className="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded mb-6" role="alert">
          <p className="font-bold">Aucune offre trouvée</p>
          <p>Essayez de modifier vos critères de recherche pour obtenir plus de résultats.</p>
        </div>
      )}
      
      {!isLoading && !error && offers && offers.length > 0 && (
        <>
          <p className="text-gray-600 mb-4">{offers.length} offres trouvées</p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {offers.map((offer) => (
              <JobCard key={`${offer.id}-${offer.title}`} offer={offer} />
            ))}
          </div>
        </>
      )}
    </div>
  );
};

export default JobsPage;
