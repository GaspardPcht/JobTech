import type { FC } from 'react';
import { Link } from 'react-router-dom';
import FeatureCard from '../components/FeatureCard';

/**
 * Home page component for JobTech Radar
 * Displays the main landing page with key features
 */
const Home: FC = () => {
  return (
    <div className="bg-gradient-to-b from-gray-50 to-white min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden py-20 sm:py-28">
        {/* Fond avec effet de dégradé et motif */}
        <div className="absolute inset-0 bg-gradient-to-b from-indigo-50 to-white opacity-70" />
        <div className="absolute inset-0 bg-[radial-gradient(#e0e7ff_1px,transparent_1px)] [background-size:20px_20px] opacity-30" />
        
        <div className="container mx-auto px-4 relative ">
          <div className="max-w-3xl mx-auto text-center mb-20 mt-32">
            {/* Titre principal */}
            <h1 className="text-5xl md:text-6xl font-bold mb-6 tracking-tight">
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 via-blue-500 to-indigo-400">
                JobTech Radar
              </span>
            </h1>
            
            {/* Slogan */}
            <p className="text-2xl md:text-3xl font-medium text-gray-800 mb-6 leading-tight">
              Votre radar pour naviguer dans l'océan des opportunités tech
            </p>
            
            {/* Description */}
            <p className="text-lg text-gray-600 mb-8 max-w-2xl mx-auto leading-relaxed">
              Trouvez les offres d'emploi qui correspondent à vos compétences et aspirations, en temps réel, directement depuis les meilleures sources du marché.
            </p>
            
            {/* Boutons avec animations fluides */}
            <div className="flex flex-col sm:flex-row justify-center gap-4">
              <Link 
                to="/jobs" 
                className="bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-3 px-8 rounded-lg transition-all duration-300 ease-in-out shadow-md hover:shadow-lg transform hover:-translate-y-1"
              >
                Explorer les offres
              </Link>
              <Link 
                to="/tech-trends" 
                className="bg-white hover:bg-gray-50 text-indigo-600 font-medium py-3 px-8 rounded-lg border border-indigo-200 transition-all duration-300 ease-in-out shadow hover:shadow-md transform hover:-translate-y-1"
              >
                Découvrir les tendances
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center text-gray-800 mb-12">Pourquoi choisir JobTech Radar ?</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
            <FeatureCard
              title="Offres en temps réel"
              description="Accédez aux dernières offres d'emploi tech directement depuis Pôle Emploi et Adzuna, sans délai ni intermédiaire."
              actionText="Explorer les offres →"
              onActionClick={() => window.location.href = '/jobs'}
            />

            <FeatureCard
              title="Analyse des tendances"
              description="Visualisez les technologies les plus demandées sur le marché et orientez votre carrière vers les compétences d'avenir."
              actionText="Voir les tendances →"
              onActionClick={() => window.location.href = '/tech-trends'}
            />

            <FeatureCard
              title="Suivi de candidatures"
              description="Organisez et suivez vos candidatures en un seul endroit pour maximiser vos chances de décrocher le job idéal."
              actionText="Gérer mes candidatures →"
              onActionClick={() => window.location.href = '/applications'}
            />
          </div>
        </div>
      </section>
      
      {/* Testimonials Section */}
      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center text-gray-800 mb-12">Ce que disent nos utilisateurs</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="flex items-center mb-4">
                <div className="h-12 w-12 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600 font-bold text-xl">S</div>
                <div className="ml-4">
                  <h3 className="font-medium">Sophie Martin</h3>
                  <p className="text-gray-600 text-sm">Développeuse Frontend</p>
                </div>
              </div>
              <p className="text-gray-700">"Grâce à JobTech Radar, j'ai pu trouver des offres correspondant exactement à mes compétences en React et Vue.js. L'interface est intuitive et les filtres sont très pertinents."</p>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="flex items-center mb-4">
                <div className="h-12 w-12 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600 font-bold text-xl">T</div>
                <div className="ml-4">
                  <h3 className="font-medium">Thomas Dubois</h3>
                  <p className="text-gray-600 text-sm">Data Scientist</p>
                </div>
              </div>
              <p className="text-gray-700">"J'apprécie particulièrement l'analyse des tendances qui m'a aidé à orienter ma formation continue vers les technologies les plus recherchées dans mon domaine."</p>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="flex items-center mb-4">
                <div className="h-12 w-12 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600 font-bold text-xl">L</div>
                <div className="ml-4">
                  <h3 className="font-medium">Lucie Bernard</h3>
                  <p className="text-gray-600 text-sm">Étudiante en informatique</p>
                </div>
              </div>
              <p className="text-gray-700">"En tant qu'étudiante, JobTech Radar m'a permis de trouver facilement des stages et alternances dans le domaine du développement web. Une ressource indispensable !"</p>
            </div>
          </div>
        </div>
      </section>
      
      {/* CTA Section */}
      <section className="py-20 bg-indigo-600">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold text-white mb-6">Prêt à booster votre carrière tech ?</h2>
          <p className="text-xl text-indigo-100 mb-10 max-w-2xl mx-auto">
            Rejoignez des milliers de professionnels qui ont trouvé leur emploi idéal grâce à JobTech Radar.
          </p>
          <Link to="/jobs" className="bg-white text-indigo-600 hover:bg-indigo-50 font-medium py-3 px-8 rounded-lg transition-colors duration-300 shadow-lg inline-block">
            Découvrir les offres maintenant
          </Link>
        </div>
      </section>
    </div>
  );
};

export default Home;
