import React, { useState } from 'react';
import axios from 'axios';
import { Lock, Mail } from 'lucide-react';

function Login({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const response = await axios.post('http://localhost:5000/login', { email, password });
      if (response.data.status === 'success') {
        onLogin(true);
      } else {
        setError('Invalid credentials');
      }
    } catch (err) {
      setError('Login failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-50 via-white to-blue-50 px-4 py-12 overflow-hidden">
      <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-r from-purple-100 to-blue-100 opacity-10 transform -skew-y-6 origin-top-left"></div>
      
      <div className="relative max-w-md w-full space-y-8 bg-white shadow-2xl rounded-2xl p-10 border border-gray-100 transform transition-all duration-300 hover:scale-[1.02] hover:shadow-3xl">
        <div className="text-center">
          <div className="flex justify-center mb-6">
            <div className="bg-gradient-to-br from-indigo-500 to-blue-600 p-4 rounded-full shadow-lg">
              <Lock className="h-10 w-10 text-white" />
            </div>
          </div>
          <h2 className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-blue-500">
             Verification
          </h2>
          <p className="mt-2 text-sm text-gray-500 tracking-wide">
            Secure Content Authentication
          </p>
        </div>
        
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="space-y-4">
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Mail className="h-5 w-5 text-gray-400" />
              </div>
              <input
                id="email"
                name="email"
                type="email"
                required
                className="pl-10 appearance-none rounded-lg relative block w-full px-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition duration-300"
                placeholder="Email address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Lock className="h-5 w-5 text-gray-400" />
              </div>
              <input
                id="password"
                name="password"
                type="password"
                required
                className="pl-10 appearance-none rounded-lg relative block w-full px-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition duration-300"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>

          {error && (
            <div className="text-center">
              <p className="text-red-500 text-sm bg-red-50 p-2 rounded-md animate-pulse">
                {error}
              </p>
            </div>
          )}

          <div>
            <button
              type="submit"
              disabled={isLoading}
              className={`group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-bold rounded-lg text-white 
                transition duration-300 ease-in-out transform hover:scale-[1.02] hover:shadow-lg
                ${isLoading 
                  ? 'bg-gradient-to-r from-gray-400 to-gray-500 cursor-not-allowed' 
                  : 'bg-gradient-to-r from-indigo-600 to-blue-500 hover:from-indigo-700 hover:to-blue-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500'
                }`}
            >
              {isLoading ? 'Authenticating...' : 'Secure Login'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default Login;