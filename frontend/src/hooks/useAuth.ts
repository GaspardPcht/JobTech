import { useContext } from 'react';
import AuthContext from '../contexts/AuthContext.js';

/**
 * Hook personnalisé pour utiliser le contexte d'authentification
 */
export const useAuth = () => useContext(AuthContext);

export default useAuth;
