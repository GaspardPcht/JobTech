import React, { useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import authService from '../services/authService';
import type { User } from '../services/authService';
import AuthContext from './AuthContext.js';

interface AuthProviderProps {
  children: ReactNode;
}

// Fournisseur du contexte d'authentification
export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);

  // Vérifier si l'utilisateur est déjà connecté au chargement de l'application
  useEffect(() => {
    const checkAuth = async () => {
      try {
        if (authService.isLoggedIn()) {
          const userData = await authService.getCurrentUser();
          setUser(userData);
          setIsAuthenticated(true);
        }
      } catch (err) {
        console.error('Erreur lors de la vérification de l\'authentification:', err);
        authService.logout();
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  // Fonction de connexion
  const login = async (email: string, password: string) => {
    setLoading(true);
    setError(null);
    try {
      await authService.login({ username: email, password });
      const userData = await authService.getCurrentUser();
      setUser(userData);
      setIsAuthenticated(true);
    } catch (err) {
      setError('Échec de la connexion. Vérifiez vos identifiants.');
      console.error('Erreur de connexion:', err);
    } finally {
      setLoading(false);
    }
  };

  // Fonction d'inscription
  const register = async (email: string, username: string, password: string) => {
    setLoading(true);
    setError(null);
    try {
      console.log('Données d\'inscription envoyées:', { email, username, password });
      await authService.register({ email, username, password });
      // Connexion automatique après inscription
      await login(email, password);
    } catch (err) {
      console.error('Erreur d\'inscription complète:', err);
      const axiosError = err as { response?: { data?: { detail?: string } } };
      if (axiosError.response?.data?.detail) {
        console.error('Détails de l\'erreur:', axiosError.response.data);
        setError(`Échec de l'inscription: ${axiosError.response.data.detail}`);
      } else {
        setError('Échec de l\'inscription. Veuillez réessayer.');
      }
    } finally {
      setLoading(false);
    }
  };

  // Fonction de déconnexion
  const logout = () => {
    authService.logout();
    setUser(null);
    setIsAuthenticated(false);
  };

  const value = {
    user,
    loading,
    error,
    login,
    register,
    logout,
    isAuthenticated,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
