"use client";

import { useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Menu, X, CheckCircle2 } from "lucide-react";

export default function Navbar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: "smooth" });
      setIsMenuOpen(false);
    }
  };

  return (
    <nav className="sticky top-0 z-50 bg-white border-b shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-500 rounded-lg flex items-center justify-center">
              <CheckCircle2 className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold text-gray-900">TaskFlow</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <button
              onClick={() => scrollToSection("features")}
              className="text-gray-700 hover:text-blue-600 transition-colors font-medium"
            >
              Features
            </button>
            <button
              onClick={() => scrollToSection("how-it-works")}
              className="text-gray-700 hover:text-blue-600 transition-colors font-medium"
            >
              How It Works
            </button>
            <button
              onClick={() => scrollToSection("pricing")}
              className="text-gray-700 hover:text-blue-600 transition-colors font-medium"
            >
              Pricing
            </button>
            <button
              onClick={() => scrollToSection("faq")}
              className="text-gray-700 hover:text-blue-600 transition-colors font-medium"
            >
              FAQ
            </button>
          </div>

          {/* Auth Buttons - Desktop */}
          <div className="hidden md:flex items-center space-x-4">
            <Link href="/signin">
              <Button variant="ghost" className="font-medium">
                Sign In
              </Button>
            </Link>
            <Link href="/signup">
              <Button className="bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 font-medium">
                Get Started
              </Button>
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden">
            <button
              onClick={toggleMenu}
              className="text-gray-700 hover:text-blue-600 transition-colors"
              aria-label="Toggle menu"
            >
              {isMenuOpen ? (
                <X className="w-6 h-6" />
              ) : (
                <Menu className="w-6 h-6" />
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {isMenuOpen && (
        <div className="md:hidden border-t bg-white">
          <div className="px-4 py-4 space-y-3">
            <button
              onClick={() => scrollToSection("features")}
              className="block w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-md font-medium"
            >
              Features
            </button>
            <button
              onClick={() => scrollToSection("how-it-works")}
              className="block w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-md font-medium"
            >
              How It Works
            </button>
            <button
              onClick={() => scrollToSection("pricing")}
              className="block w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-md font-medium"
            >
              Pricing
            </button>
            <button
              onClick={() => scrollToSection("faq")}
              className="block w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-md font-medium"
            >
              FAQ
            </button>
            <div className="pt-4 space-y-2">
              <Link href="/signin" className="block">
                <Button variant="outline" className="w-full font-medium">
                  Sign In
                </Button>
              </Link>
              <Link href="/signup" className="block">
                <Button className="w-full bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 font-medium">
                  Get Started
                </Button>
              </Link>
            </div>
          </div>
        </div>
      )}
    </nav>
  );
}
