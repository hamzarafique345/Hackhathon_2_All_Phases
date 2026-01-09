"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useAuth } from "@/components/auth/AuthContext";
import apiClient from "@/lib/api-client";
import { AlertCircle, Loader2 } from "lucide-react";

interface SignInFormData {
  email: string;
  password: string;
  rememberMe: boolean;
}

interface SignInResponse {
  user: {
    id: string;
    email: string;
    name: string | null;
    created_at: string;
  };
  token: string;
  expiresAt: string;
}

export default function SignInPage() {
  const router = useRouter();
  const { login } = useAuth();

  const [formData, setFormData] = useState<SignInFormData>({
    email: "",
    password: "",
    rememberMe: false,
  });

  const [errors, setErrors] = useState<Partial<SignInFormData>>({});
  const [apiError, setApiError] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);

  // Handle input changes
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
    // Clear error for this field when user starts typing
    setErrors((prev) => ({ ...prev, [name]: "" }));
    setApiError("");
  };

  // Validate form
  const validateForm = (): boolean => {
    const newErrors: Partial<SignInFormData> = {};

    // Email validation
    if (!formData.email) {
      newErrors.email = "Email is required";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = "Please enter a valid email address";
    }

    // Password validation
    if (!formData.password) {
      newErrors.password = "Password is required";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setApiError("");

    // Validate form
    if (!validateForm()) {
      return;
    }

    setIsLoading(true);

    try {
      // Call backend API
      const response = await apiClient.post<SignInResponse>("/auth/signin", {
        email: formData.email,
        password: formData.password,
        rememberMe: formData.rememberMe,
      });

      // Store token and user data
      login(response.data.token, response.data.user);

      // Redirect to dashboard
      router.push("/dashboard");
    } catch (error: any) {
      // Handle API errors
      if (error.response?.status === 401) {
        setApiError("Invalid email or password. Please try again.");
      } else if (error.response?.data?.detail) {
        setApiError(error.response.data.detail);
      } else {
        setApiError("An error occurred. Please try again later.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-600 via-purple-600 to-blue-800 px-4 py-8 relative overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-blue-500 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-2000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-pink-500 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-4000"></div>
      </div>

      <Card className="w-full max-w-md relative z-10 shadow-2xl animate-fade-in-up">
        <CardHeader className="space-y-1">
          <CardTitle className="text-2xl font-bold text-center animate-fade-in">Welcome back</CardTitle>
          <CardDescription className="text-center animate-fade-in animation-delay-200">
            Sign in to your account to continue
          </CardDescription>
        </CardHeader>
        <CardContent className="animate-fade-in animation-delay-400">
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* API Error Message */}
            {apiError && (
              <div className="flex items-center gap-2 p-3 text-sm text-red-800 bg-red-50 border border-red-200 rounded-md animate-shake">
                <AlertCircle className="w-4 h-4 flex-shrink-0" />
                <span>{apiError}</span>
              </div>
            )}

            {/* Email Field */}
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                name="email"
                type="email"
                placeholder="you@example.com"
                value={formData.email}
                onChange={handleChange}
                disabled={isLoading}
                className={errors.email ? "border-red-500" : ""}
              />
              {errors.email && (
                <p className="text-sm text-red-600">{errors.email}</p>
              )}
            </div>

            {/* Password Field */}
            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                name="password"
                type="password"
                placeholder="••••••••"
                value={formData.password}
                onChange={handleChange}
                disabled={isLoading}
                className={errors.password ? "border-red-500" : ""}
              />
              {errors.password && (
                <p className="text-sm text-red-600">{errors.password}</p>
              )}
            </div>

            {/* Remember Me Checkbox */}
            <div className="flex items-center space-x-2">
              <input
                id="rememberMe"
                name="rememberMe"
                type="checkbox"
                checked={formData.rememberMe}
                onChange={handleChange}
                disabled={isLoading}
                className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
              />
              <Label htmlFor="rememberMe" className="text-sm font-normal cursor-pointer">
                Remember me for 7 days
              </Label>
            </div>

            {/* Submit Button */}
            <Button
              type="submit"
              className="w-full bg-blue-600 hover:bg-blue-700 transition-all duration-300 hover:scale-105 hover:shadow-lg"
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Signing in...
                </>
              ) : (
                "Sign In"
              )}
            </Button>
          </form>

          {/* Sign Up Link */}
          <div className="mt-4 text-center text-sm">
            Don't have an account?{" "}
            <Link href="/signup" className="text-blue-600 hover:underline font-medium transition-all duration-200 hover:text-blue-700">
              Sign up
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
