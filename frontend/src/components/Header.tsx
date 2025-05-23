import type { FC } from 'react';

/**
 * Header component for JobTech Radar application
 * Displays the main navigation and branding
 */
const Header: FC = () => {
  return (
    <header className="sticky top-0 z-10 bg-white shadow-sm">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        {/* Logo and brand name */}
        <div className="flex items-center space-x-2">
          <span className="text-primary font-bold text-2xl">JobTech Radar</span>
        </div>
        
        {/* Main navigation */}
        <nav className="hidden md:flex space-x-6">
          <a href="/" className="text-textPrimary hover:text-primary transition-colors">
            Accueil
          </a>
          <a href="/jobs" className="text-textSecondary hover:text-primary transition-colors">
            Offres d'emploi
          </a>
          <a href="/tech-trends" className="text-textSecondary hover:text-primary transition-colors">
            Tendances Tech
          </a>
          <a href="/applications" className="text-textSecondary hover:text-primary transition-colors">
            Mes candidatures
          </a>
        </nav>
        
        {/* User actions */}
        <div className="flex items-center space-x-4">
          <button className="bg-primary text-white px-4 py-2 rounded-md hover:bg-opacity-90 transition-colors">
            Connexion
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;
