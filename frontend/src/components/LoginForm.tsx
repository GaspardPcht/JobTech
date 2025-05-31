import React, { useState } from 'react';
import useAuth from '../hooks/useAuth';
import Button from './Button';
import { IoEyeOff, IoEye } from 'react-icons/io5';

const LoginForm: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { login, error, loading } = useAuth();
  const [isPasswordVisible, setIsPasswordVisible] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await login(email, password);
  };

  return (
    <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Connexion</h2>
      
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
            placeholder="Email"
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
            required
          />
        </div>
        
        <div className="mb-6">
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
        </div>
        
        <Button 
          type="submit" 
          variant="primary" 
          fullWidth 
          disabled={loading}
        >
          {loading ? 'Connexion en cours...' : 'Se connecter'}
        </Button>
      </form>
    </div>
  );
};

export default LoginForm;
