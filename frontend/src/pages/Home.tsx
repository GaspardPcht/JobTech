import type { FC } from 'react';
import FeatureCard from '../components/FeatureCard';

/**
 * Home page component for JobTech Radar
 * Displays the main landing page with key features
 */
const Home: FC = () => {
  return (
    <main className="container mx-auto px-4 py-8">
      <section className="mb-12">
        <h1 className="text-4xl font-bold text-textPrimary mb-4">
          Bienvenue sur JobTech Radar
        </h1>
        <p className="text-textSecondary text-xl max-w-3xl">
          La plateforme qui aide les développeurs et étudiants tech à trouver des opportunités
          d'emploi pertinentes et suivre les tendances du marché.
        </p>
      </section>

      <section className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        <FeatureCard
          title="Offres d'emploi"
          description="Trouvez des offres d'emploi pertinentes basées sur vos compétences et préférences."
          actionText="Explorer les offres →"
          onActionClick={() => console.log('Navigation vers les offres d\'emploi')}
        />

        <FeatureCard
          title="Tendances Tech"
          description="Découvrez les technologies les plus demandées sur le marché du travail."
          actionText="Voir les tendances →"
          onActionClick={() => console.log('Navigation vers les tendances tech')}
        />

        <FeatureCard
          title="Suivi de candidatures"
          description="Organisez et suivez vos candidatures en un seul endroit."
          actionText="Gérer mes candidatures →"
          onActionClick={() => console.log('Navigation vers le suivi de candidatures')}
        />
      </section>
    </main>
  );
};

export default Home;
