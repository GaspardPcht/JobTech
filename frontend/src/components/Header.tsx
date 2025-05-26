import type { FC } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import Button from './Button';
import useAuth from '../hooks/useAuth';

/**
 * Header component for JobTech Radar application
 * Displays the main navigation and branding
 */
const Header: FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { isAuthenticated, user, logout } = useAuth();
  
  // Fonction pour déterminer si un lien est actif
  const isActive = (path: string) => location.pathname === path;
  
  // Fonction pour gérer la déconnexion
  const handleLogout = () => {
    logout();
    navigate('/');
  };
  
  return (
    <header className="sticky top-0 z-10 bg-white shadow-sm">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        {/* Logo and brand name */}
        <div className="flex items-center space-x-2">
          <Link to="/" className="text-indigo-600 font-bold text-2xl">JobTech Radar</Link>
        </div>
        
        {/* Main navigation */}
        <nav className="hidden md:flex space-x-6">
          <Link 
            to="/" 
            className={`${isActive('/') ? 'text-indigo-600 font-medium' : 'text-gray-700'} hover:text-indigo-600 transition-colors`}
          >
            Accueil
          </Link>
          <Link 
            to="/jobs" 
            className={`${isActive('/jobs') ? 'text-indigo-600 font-medium' : 'text-gray-700'} hover:text-indigo-600 transition-colors`}
          >
            Offres d'emploi
          </Link>
          <Link 
            to="/tech-trends" 
            className={`${isActive('/tech-trends') ? 'text-indigo-600 font-medium' : 'text-gray-700'} hover:text-indigo-600 transition-colors`}
          >
            Tendances Tech
          </Link>
          <Link 
            to="/applications" 
            className={`${isActive('/applications') ? 'text-indigo-600 font-medium' : 'text-gray-700'} hover:text-indigo-600 transition-colors`}
          >
            Mes candidatures
          </Link>
        </nav>
        
        {/* User actions */}
        <div className="flex items-center space-x-4">
          {isAuthenticated ? (
            <>
              <span className="text-gray-700 mr-2">
                Bonjour, {user?.username}
              </span>
              <Button variant="outline" size="md" onClick={handleLogout}>
                Déconnexion
              </Button>
            </>
          ) : (
            <>
              <Button variant="outline" size="md" onClick={() => navigate('/login')}>
                Connexion
              </Button>
              <Button variant="primary" size="md" onClick={() => navigate('/register')}>
                S'inscrire
              </Button>
            </>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;
