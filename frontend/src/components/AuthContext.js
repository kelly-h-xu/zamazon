// IMPORTS
import React, { createContext, useState, useEffect } from "react";
import axios from "axios";

import { baseURL } from "../config";

// Create a context for authentication
export const AuthContext = createContext();

// AUTH PROVIDER
export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(
    () => JSON.parse(localStorage.getItem("isAuthenticated")) || false
  );

  // Updates authentication status
  const setAuthStatus = (status) => {
    setIsAuthenticated(status);
    localStorage.setItem("isAuthenticated", JSON.stringify(status));
  };

  // Initial authentication check with the backend
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const response = await axios.get(`${baseURL}/auth-check`, {
          withCredentials: true,
        });
        if (response.status === 200) {
          setAuthStatus(true);
        } else {
          setAuthStatus(false);
        }
      } catch (error) {
        console.error("Auth check failed:", error);
        setAuthStatus(false);
      }
    };
    checkAuth();
  }, []);

  // Logout handling
  const logout = async () => {
    try {
      await axios.post(`${baseURL}/logout`, {}, { withCredentials: true });
      setAuthStatus(false); // Update the authentication state in context
    } catch (error) {
      console.error("Logout failed:", error);
    }
  };

  // Return authentication state and functions to child components via context
  return (
    <AuthContext.Provider value={{ isAuthenticated, setAuthStatus, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
export default AuthProvider;
