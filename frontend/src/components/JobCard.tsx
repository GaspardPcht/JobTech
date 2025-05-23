import React from 'react';
import type { Offer } from '../types/offer';
import { formatSalary, formatContractType } from '../services/offerService';

interface JobCardProps {
  offer: Offer;
}

const JobCard: React.FC<JobCardProps> = ({ offer }) => {
  // Formater la date de publication
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('fr-FR', { 
      day: 'numeric', 
      month: 'short', 
      year: 'numeric' 
    }).format(date);
  };

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
      <div className="p-6">
        <div className="flex justify-between items-start">
          <h3 className="text-xl font-semibold text-indigo-600 mb-2 flex-1">{offer.title}</h3>
          {offer.remote && (
            <span className="bg-emerald-100 text-emerald-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
              Remote
            </span>
          )}
        </div>
        
        <div className="flex items-center text-gray-600 mb-4">
          <span className="font-medium">{offer.company}</span>
          <span className="mx-2">•</span>
          <span>{offer.location}</span>
        </div>
        
        <div className="mb-4 text-sm text-gray-700 line-clamp-3">
          {offer.description}
        </div>
        
        <div className="flex flex-wrap gap-2 mb-4">
          {offer.techs.map((tech) => (
            <span 
              key={tech.id} 
              className="bg-indigo-100 text-indigo-800 text-xs font-medium px-2.5 py-0.5 rounded"
            >
              {tech.name}
            </span>
          ))}
        </div>
        
        <div className="flex justify-between items-center text-sm text-gray-600">
          <div>
            <span className="font-medium">{formatContractType(offer.contract_type)}</span>
            {(offer.salary_min || offer.salary_max) && (
              <>
                <span className="mx-2">•</span>
                <span>{formatSalary(offer.salary_min, offer.salary_max)}</span>
              </>
            )}
          </div>
          <div>
            Publié le {formatDate(offer.posted_at)}
          </div>
        </div>
        
        <div className="mt-4 flex justify-between items-center">
          <a 
            href={offer.url} 
            target="_blank" 
            rel="noopener noreferrer" 
            className="text-indigo-600 hover:text-indigo-800 font-medium text-sm"
          >
            Voir l'offre
          </a>
          <button 
            className="bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded-md text-sm transition-colors duration-300"
            onClick={() => window.open(offer.url, '_blank')}
          >
            Postuler
          </button>
        </div>
      </div>
    </div>
  );
};

export default JobCard;
