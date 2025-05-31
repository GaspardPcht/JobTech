import React, { useState } from 'react';
import useAuth from '../hooks/useAuth';
import Button from './Button';
import { IoEye, IoEyeOff } from 'react-icons/io5';

const RegisterForm: React.FC = () => {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [passwordError, setPasswordError] = useState('');
  const [isPasswordVisible, setIsPasswordVisible] = useState(false);
  const [isConfirmPasswordVisible, setIsConfirmPasswordVisible] = useState(false);
  const { register, error, loading } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Vérifier que les mots de passe correspondent
    if (password !== confirmPassword) {
      setPasswordError('Les mots de passe ne correspondent pas');
      return;
    }
    
    setPasswordError('');
    await register(email, username, password);
  };

  return (
    <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Créer un compte</h2>
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4" role="alert">
          <span className="block sm:inline">{error}</span>
        </div>
      )}
      
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="email" className="block text-gray-700 text-sm font-medium mb-2">
            Email
          </label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
            required
          />
        </div>
        
        <div className="mb-4">
          <label htmlFor="username" className="block text-gray-700 text-sm font-medium mb-2">
            Nom d'utilisateur
          </label>
          <input
            id="username"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
            required
            minLength={3}
          />
        </div>
        
        <div className="mb-4">
          <label htmlFor="password" className="block text-gray-700 text-sm font-medium mb-2">
            Mot de passe
          </label>
          <div className="relative">
            <input
              id="password"
              type={isPasswordVisible ? "text" : "password"}
              value={password}
              placeholder="Mot de passe"
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 pr-10 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
              required
              minLength={8}
            />
            <div 
              className="absolute inset-y-0 right-0 flex items-center pr-3 cursor-pointer" 
              onClick={() => setIsPasswordVisible(!isPasswordVisible)}
            >
              {isPasswordVisible ? 
                <IoEye className="text-gray-500 text-xl" /> : 
                <IoEyeOff className="text-gray-500 text-xl" />}
            </div>
          </div>
          <p className="text-xs text-gray-500 mt-1">Le mot de passe doit contenir au moins 8 caractères</p>
        </div>
        
        <div className="mb-6">
          <label htmlFor="confirmPassword" className="block text-gray-700 text-sm font-medium mb-2">
            Confirmer le mot de passe
          </label>
          <div className="relative">
            <input
              id="confirmPassword"
              type={isConfirmPasswordVisible ? "text" : "password"}
              value={confirmPassword}
              placeholder="Confirmer le mot de passe"
              onChange={(e) => setConfirmPassword(e.target.value)}
              className="w-full px-3 py-2 pr-10 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
              required
            />
            <div 
              className="absolute inset-y-0 right-0 flex items-center pr-3 cursor-pointer" 
              onClick={() => setIsConfirmPasswordVisible(!isConfirmPasswordVisible)}
            >
              {isConfirmPasswordVisible ? 
                <IoEye className="text-gray-500 text-xl" /> : 
                <IoEyeOff className="text-gray-500 text-xl" />}
            </div>
          </div>
          {passwordError && (
            <p className="text-xs text-red-500 mt-1">{passwordError}</p>
          )}
        </div>
        
        <Button 
          type="submit" 
          variant="primary" 
          fullWidth 
          disabled={loading}
        >
          {loading ? 'Inscription en cours...' : 'S\'inscrire'}
        </Button>
      </form>
    </div>
  );
};

export default RegisterForm;
