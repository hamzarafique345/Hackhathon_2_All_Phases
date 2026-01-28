"use client";

/**
 * AuthContext - Global authentication state management
 * Provides user authentication state and methods throughout the app
 */
import React, { createContext, useContext, useState, useEffect, ReactNode } from "react";
import apiClient from "@/lib/api-client";

// User type definition
export interface User {
  id: string;
  email: string;
  name: string | null;
  created_at: string;
}

// Auth context type definition
interface AuthContextType {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (token: string, user: User) => void;
  logout: () => void;
  verifyToken: () => Promise<void>;
}

// Create context with undefined default
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// AuthProvider component
export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Verify token on mount
  useEffect(() => {
    const initAuth = async () => {
      const storedToken = localStorage.getItem("auth_token");

      if (storedToken) {
        setToken(storedToken);
        await verifyToken();
      } else {
        setIsLoading(false);
      }
    };

    initAuth();
  }, []);

  // Verify token with backend
  const verifyToken = async () => {
    try {
      const response = await apiClient.get<User>("/auth/verify");
      setUser(response.data);
    } catch (error) {
      // Token is invalid, clear it
      localStorage.removeItem("auth_token");
      setToken(null);
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  };

  // Login method
  const login = (newToken: string, newUser: User) => {
    localStorage.setItem("auth_token", newToken);
    setToken(newToken);
    setUser(newUser);
  };

  // Logout method
  const logout = () => {
    localStorage.removeItem("auth_token");
    setToken(null);
    setUser(null);
  };

  const value: AuthContextType = {
    user,
    token,
    isLoading,
    isAuthenticated: !!user && !!token,
    login,
    logout,
    verifyToken,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

// Custom hook to use auth context
export function useAuth() {
  const context = useContext(AuthContext);

  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }

  return context;
}
