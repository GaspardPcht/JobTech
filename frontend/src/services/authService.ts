import axios from 'axios';

// Utilisez le port configuré ou 8000 par défaut
const API_PORT = import.meta.env.VITE_API_PORT || '8000';
const API_URL = `http://localhost:${API_PORT}/api/auth`;

// Types
export interface UserRegister {
  email: string;
  username: string;
  password: string;
}

export interface UserLogin {
  username: string;
  password: string;
}

export interface User {
  id: number;
  email: string;
  username: string;
  is_active: boolean;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

/**
 * Service pour gérer l'authentification avec le backend
 */
const authService = {
  /**
   * Inscription d'un nouvel utilisateur
   */
  register: async (userData: UserRegister): Promise<User> => {
    
    // Utiliser le format JSON standard pour l'inscription
    try {
      const response = await axios.post(`${API_URL}/register`, userData, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      return response.data;
    } catch (error: any) {
      console.error('Erreur détaillée:', error);
      if (error.response) {
        // La requête a été faite et le serveur a répondu avec un code d'état
        // qui n'est pas dans la plage 2xx
        console.error('Données de réponse d\'erreur:', error.response.data);
        console.error('Statut:', error.response.status);
        console.error('En-têtes:', error.response.headers);
      } else if (error.request) {
        // La requête a été faite mais aucune réponse n'a été reçue
        console.error('Requête sans réponse:', error.request);
      } else {
        // Une erreur s'est produite lors de la configuration de la requête
        console.error('Erreur de configuration:', error.message);
      }
      throw error;
    }
  },

  /**
   * Connexion d'un utilisateur
   */
  login: async (credentials: UserLogin): Promise<AuthResponse> => {
    // Pour FastAPI, nous devons envoyer les données de connexion sous forme de FormData
    const formData = new FormData();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    const response = await axios.post(`${API_URL}/login`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    // Stocker le token dans le localStorage
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
    }
    
    return response.data;
  },

  /**
   * Récupération des informations de l'utilisateur connecté
   */
  getCurrentUser: async (): Promise<User> => {
    const token = localStorage.getItem('token');
    
    if (!token) {
      throw new Error('Aucun utilisateur connecté');
    }
    
    const response = await axios.get(`${API_URL}/me`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    return response.data;
  },

  /**
   * Déconnexion de l'utilisateur
   */
  logout: (): void => {
    localStorage.removeItem('token');
  },

  /**
   * Vérifie si un utilisateur est connecté
   */
  isLoggedIn: (): boolean => {
    return !!localStorage.getItem('token');
  },

  /**
   * Récupère le token d'authentification
   */
  getToken: (): string | null => {
    return localStorage.getItem('token');
  }
};

export default authService;
