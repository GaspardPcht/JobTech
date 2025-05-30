import React from 'react';
import { useTechTrends, useSyncTechs } from '../hooks/useTechStats';
import TechTrendCard from '../components/TechTrendCard';

/**
 * Page des tendances technologiques affichant le top 10 des technologies les plus demandées
 * Design moderne suivant les directives de style JobTech Radar
 */
const TechTrendsPage: React.FC = () => {
  // Récupérer les données des tendances (limité à 10)
  const { 
    data: trends, 
    isLoading: trendsLoading, 
    error: trendsError,
    refetch: refetchTrends
  } = useTechTrends(10);
  
  // Mutation pour synchroniser les technologies
  const { mutate: syncTechs, isPending: isSyncing } = useSyncTechs();
  
  const handleSyncTechs = async () => {
    await syncTechs();
    refetchTrends();
  };
  
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      <div className="container mx-auto px-4 py-12">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-10">
          <div>
            <h1 className="text-4xl font-bold text-gray-900 mb-2">Top 10 Technologies</h1>
            <p className="text-gray-600 text-lg">Les technologies les plus demandées sur le marché de l'emploi</p>
          </div>
          <button
            onClick={handleSyncTechs}
            disabled={isSyncing}
            className="bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2.5 px-5 rounded-lg flex items-center gap-2 shadow-md hover:shadow-lg transition-all disabled:opacity-70 disabled:cursor-not-allowed"
          >
            {isSyncing ? (
              <>
                <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>Synchronisation en cours...</span>
              </>
            ) : (
              <>
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                <span>Synchroniser les technologies</span>
              </>
            )}
          </button>
        </div>
      
        {/* Affichage des erreurs */}
        {trendsError && (
          <div className="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 rounded-lg mb-8 shadow-sm" role="alert">
            <div className="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p className="font-medium">Erreur lors du chargement des tendances. Veuillez réessayer.</p>
            </div>
          </div>
        )}
        
        {/* Affichage des tendances */}
        {trendsLoading ? (
          <div className="flex flex-col justify-center items-center h-64 gap-4">
            <div className="animate-spin rounded-full h-14 w-14 border-t-2 border-b-2 border-indigo-600"></div>
            <p className="text-gray-600 font-medium">Chargement des tendances...</p>
          </div>
        ) : (
          <>
            {trends && trends.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {trends.map((trend, index) => (
                  <TechTrendCard key={trend.name} trend={trend} rank={index + 1} />
                ))}
              </div>
            ) : (
              <div className="bg-white rounded-xl shadow-lg p-10 text-center">
                <div className="flex flex-col items-center gap-4">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                  <h3 className="text-xl font-bold text-gray-800">Aucune tendance technologique disponible</h3>
                  <p className="text-gray-600 max-w-md">
                    Cliquez sur le bouton "Synchroniser les technologies" pour analyser les offres d'emploi et générer les tendances.
                  </p>
                  <button
                    onClick={handleSyncTechs}
                    disabled={isSyncing}
                    className="mt-4 bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded-lg transition-colors"
                  >
                    {isSyncing ? 'Synchronisation...' : 'Synchroniser maintenant'}
                  </button>
                </div>
              </div>
            )}
          </>
        )}
        
        {/* Informations sur les tendances */}
        {!trendsLoading && trends && trends.length > 0 && (
          <div className="mt-12 bg-white rounded-xl shadow-md p-6 border border-gray-100">
            <h2 className="text-xl font-bold text-gray-800 mb-4">Comment utiliser ces données ?</h2>
            <p className="text-gray-600 mb-3">
              Ces tendances sont calculées à partir des offres d'emploi analysées par JobTech Radar. Elles vous permettent d'identifier les technologies les plus demandées sur le marché du travail.            
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
              <div className="bg-indigo-50 p-4 rounded-lg">
                <h3 className="font-medium text-indigo-800 mb-2">Orientation de carrière</h3>
                <p className="text-gray-600 text-sm">Utilisez ces données pour orienter votre apprentissage vers les technologies les plus recherchées.</p>
              </div>
              <div className="bg-indigo-50 p-4 rounded-lg">
                <h3 className="font-medium text-indigo-800 mb-2">Compétitivité sur le marché</h3>
                <p className="text-gray-600 text-sm">Comprenez quelles compétences vous démarquent et lesquelles sont devenues standard.</p>
              </div>
              <div className="bg-indigo-50 p-4 rounded-lg">
                <h3 className="font-medium text-indigo-800 mb-2">Tendances émergentes</h3>
                <p className="text-gray-600 text-sm">Identifiez les technologies en croissance pour anticiper les besoins futurs du marché.</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default TechTrendsPage;
