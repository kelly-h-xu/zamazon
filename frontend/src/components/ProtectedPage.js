// IMPORTS
import React, { useContext } from 'react';
import { Navigate } from 'react-router-dom';

import { AuthContext } from './AuthContext';

//PROTECTED PAGE 
const ProtectedPage = ({ children }) => {
  // Check if the user is authenticated
  const { isAuthenticated } = useContext(AuthContext);

  // If authenticated: render data
  // If not: navigate to login
  return isAuthenticated ? children : <Navigate to="/login" />;
};

export default ProtectedPage;
