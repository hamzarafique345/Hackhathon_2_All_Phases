/**
 * Axios API client with JWT interceptors
 * Handles all backend API communication
 */
import axios, { AxiosError, InternalAxiosRequestConfig } from "axios";

// Create Axios instance with base configuration
export const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 10000, // 10 second timeout
});

// Request interceptor: Attach JWT token to all requests
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // Get token from localStorage
    const token = typeof window !== "undefined" ? localStorage.getItem("auth_token") : null;

    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

// Response interceptor: Handle 401 errors and redirect to sign-in
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error: AxiosError) => {
    // Handle 401 Unauthorized errors
    if (error.response?.status === 401) {
      // Clear token from localStorage
      if (typeof window !== "undefined") {
        localStorage.removeItem("auth_token");

        // Redirect to sign-in page if not already there
        if (window.location.pathname !== "/signin") {
          window.location.href = "/signin";
        }
      }
    }

    return Promise.reject(error);
  }
);

// Export typed API methods
export default apiClient;
