import { createContext } from 'react';
import type { AuthContextType } from './AuthContextTypes.js';

// Création du contexte avec une valeur par défaut
const AuthContext = createContext<AuthContextType>({
  user: null,
  loading: false,
  error: null,
  login: async () => {},
  register: async () => {},
  logout: () => {},
  isAuthenticated: false,
});

export default AuthContext;
