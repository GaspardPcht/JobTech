import React, { useState } from 'react';
import JobCard from '../components/JobCard';
import JobSearchForm from '../components/JobSearchForm';
import { useExternalOffers } from '../hooks/useExternalOffers';
import type { OfferFilters, Offer } from '../types/offer';

const JobsPage: React.FC = () => {
  const [allOffers, setAllOffers] = useState<Offer[]>([]);
  const [currentPage, setCurrentPage] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const [isLoadingMore, setIsLoadingMore] = useState(false);
  
  const [filters, setFilters] = useState<OfferFilters>({
    keywords: '',
    location: '',
    sources: 'all',
    limit: 50,
    sort_by: 'date', // Tri par date par défaut (plus récent en premier)
    page: 0
  });

  const { data: offers, isLoading, error, refetch } = useExternalOffers(filters);

  // Mettre à jour les offres lorsque les données sont chargées
  React.useEffect(() => {
    if (offers && !isLoading) {
      if (filters.page === 0) {
        // Première page: remplacer toutes les offres
        setAllOffers(offers);
      } else {
        // Pages suivantes: ajouter aux offres existantes
        setAllOffers(prev => [...prev, ...offers]);
      }
      
      // Vérifier s'il y a plus d'offres à charger
      setHasMore(offers.length === filters.limit);
      setIsLoadingMore(false);
    }
  }, [offers, isLoading, filters.page, filters.limit]);

  const handleSearch = (newFilters: OfferFilters) => {
    // Réinitialiser la pagination lors d'une nouvelle recherche
    const updatedFilters = {
      ...newFilters,
      page: 0
    };
    setCurrentPage(0);
    setFilters(updatedFilters);
    setAllOffers([]);
    refetch();
  };
  
  const loadMore = () => {
    setIsLoadingMore(true);
    const nextPage = currentPage + 1;
    setCurrentPage(nextPage);
    setFilters(prev => ({
      ...prev,
      page: nextPage
    }));
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
      
      {!isLoading && !error && allOffers && allOffers.length > 0 && (
        <>
          <p className="text-gray-600 mb-4">{allOffers.length} offres trouvées</p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {allOffers.map((offer, index) => (
              <JobCard key={`${offer.id}-${offer.title}-${index}`} offer={offer} />
            ))}
          </div>
          
          {hasMore && (
            <div className="flex justify-center mt-8 mb-4">
              <button
                onClick={loadMore}
                disabled={isLoadingMore}
                className="bg-indigo-600 text-white px-6 py-3 rounded-md hover:bg-indigo-700 transition-colors disabled:bg-indigo-300"
              >
                {isLoadingMore ? (
                  <span className="flex items-center">
                    <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Chargement...
                  </span>
                ) : (
                  'Charger plus d\'offres'
                )}
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default JobsPage;
