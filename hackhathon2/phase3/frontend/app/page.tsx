"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { CheckCircle2, Shield, Zap, Filter, Smartphone, RefreshCw } from "lucide-react";

export default function LandingPage() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section id="home" className="relative overflow-hidden bg-gradient-to-br from-blue-600 via-purple-600 to-pink-600 text-white">
        <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10"></div>

        {/* Animated background blobs */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute top-20 left-10 w-72 h-72 bg-blue-400 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob"></div>
          <div className="absolute top-40 right-10 w-72 h-72 bg-purple-400 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob animation-delay-2000"></div>
          <div className="absolute bottom-20 left-1/3 w-72 h-72 bg-pink-400 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob animation-delay-4000"></div>
        </div>

        <div className="relative max-w-7xl mx-auto px-4 py-20 md:py-32">
          <div className="text-center space-y-8">
            <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold tracking-tight animate-fade-in-down">
              Organize Your Life,
              <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-200 to-pink-200 animate-pulse-glow">
                One Task at a Time
              </span>
            </h1>

            <p className="text-xl md:text-2xl text-blue-100 max-w-3xl mx-auto leading-relaxed animate-fade-in-up animation-delay-200">
              The simple, powerful todo app that helps you stay organized and productive.
              Join thousands of users managing their tasks effortlessly.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center pt-8 animate-fade-in-up animation-delay-400">
              <Link href="/signup">
                <Button
                  size="lg"
                  className="w-full sm:w-auto bg-white text-blue-600 hover:bg-blue-50 font-semibold px-8 py-6 text-lg shadow-xl hover:shadow-2xl transition-all duration-300 hover:scale-110 hover:-translate-y-1"
                >
                  Get Started Free
                </Button>
              </Link>
              <Link href="/signin">
                <Button
                  size="lg"
                  variant="outline"
                  className="w-full sm:w-auto border-2 border-white text-black hover:bg-white/80 font-semibold px-8 py-6 text-lg transition-all duration-300 hover:scale-110 hover:-translate-y-1"
                >
                  Sign In
                </Button>
              </Link>
            </div>

            {/* Social Proof */}
            <div className="flex flex-wrap items-center justify-center gap-8 pt-12 text-blue-100 animate-fade-in-up animation-delay-600">
              <div className="text-center transform transition-all duration-300 hover:scale-110">
                <div className="text-3xl md:text-4xl font-bold">10,000+</div>
                <div className="text-sm md:text-base">Active Users</div>
              </div>
              <div className="text-center transform transition-all duration-300 hover:scale-110">
                <div className="text-3xl md:text-4xl font-bold">50,000+</div>
                <div className="text-sm md:text-base">Tasks Completed</div>
              </div>
              <div className="text-center transform transition-all duration-300 hover:scale-110">
                <div className="text-3xl md:text-4xl font-bold">4.9/5</div>
                <div className="text-sm md:text-base">User Rating</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 md:py-24 px-4 bg-gray-50">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl md:text-5xl font-bold text-center mb-4 text-gray-900 animate-fade-in-up">
            Why Choose TaskFlow?
          </h2>
          <p className="text-xl text-gray-600 text-center mb-16 max-w-3xl mx-auto animate-fade-in-up animation-delay-200">
            Everything you need to stay organized and productive, all in one place
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <Card className="border-2 hover:shadow-xl transition-all duration-500 hover:-translate-y-2 animate-fade-in-up animation-delay-200 hover:border-blue-300">
              <CardHeader>
                <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center mb-4 transform transition-all duration-300 hover:scale-110 hover:rotate-6">
                  <CheckCircle2 className="w-6 h-6 text-white" />
                </div>
                <CardTitle className="text-xl">Simple & Intuitive</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base">
                  Clean, user-friendly interface designed for maximum productivity.
                  Add, edit, and complete tasks with just a few clicks.
                </CardDescription>
              </CardContent>
            </Card>

            {/* Feature 2 */}
            <Card className="border-2 hover:shadow-xl transition-all duration-500 hover:-translate-y-2 animate-fade-in-up animation-delay-400 hover:border-purple-300">
              <CardHeader>
                <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-purple-600 rounded-lg flex items-center justify-center mb-4 transform transition-all duration-300 hover:scale-110 hover:rotate-6">
                  <Shield className="w-6 h-6 text-white" />
                </div>
                <CardTitle className="text-xl">Secure & Private</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base">
                  Your data is protected with industry-standard encryption.
                  JWT authentication ensures your tasks remain private and secure.
                </CardDescription>
              </CardContent>
            </Card>

            {/* Feature 3 */}
            <Card className="border-2 hover:shadow-xl transition-all duration-500 hover:-translate-y-2 animate-fade-in-up animation-delay-600 hover:border-pink-300">
              <CardHeader>
                <div className="w-12 h-12 bg-gradient-to-br from-pink-500 to-pink-600 rounded-lg flex items-center justify-center mb-4 transform transition-all duration-300 hover:scale-110 hover:rotate-6">
                  <Zap className="w-6 h-6 text-white" />
                </div>
                <CardTitle className="text-xl">Fast & Reliable</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base">
                  Built with modern technologies for lightning-fast performance.
                  Access your tasks anytime, anywhere with 99.9% uptime.
                </CardDescription>
              </CardContent>
            </Card>

            {/* Feature 4 */}
            <Card className="border-2 hover:shadow-xl transition-all duration-500 hover:-translate-y-2 animate-fade-in-up animation-delay-800 hover:border-green-300">
              <CardHeader>
                <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-green-600 rounded-lg flex items-center justify-center mb-4 transform transition-all duration-300 hover:scale-110 hover:rotate-6">
                  <Filter className="w-6 h-6 text-white" />
                </div>
                <CardTitle className="text-xl">Smart Organization</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base">
                  Filter and categorize your tasks effortlessly. View all, active, or completed
                  tasks with a single click to stay focused.
                </CardDescription>
              </CardContent>
            </Card>

            {/* Feature 5 */}
            <Card className="border-2 hover:shadow-xl transition-all duration-500 hover:-translate-y-2 animate-fade-in-up animation-delay-1000 hover:border-orange-300">
              <CardHeader>
                <div className="w-12 h-12 bg-gradient-to-br from-orange-500 to-orange-600 rounded-lg flex items-center justify-center mb-4 transform transition-all duration-300 hover:scale-110 hover:rotate-6">
                  <Smartphone className="w-6 h-6 text-white" />
                </div>
                <CardTitle className="text-xl">Cross-Platform</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base">
                  Access your tasks from any device - desktop, tablet, or mobile.
                  Fully responsive design ensures a seamless experience everywhere.
                </CardDescription>
              </CardContent>
            </Card>

            {/* Feature 6 */}
            <Card className="border-2 hover:shadow-xl transition-all duration-500 hover:-translate-y-2 animate-fade-in-up animation-delay-1000 hover:border-red-300">
              <CardHeader>
                <div className="w-12 h-12 bg-gradient-to-br from-red-500 to-red-600 rounded-lg flex items-center justify-center mb-4 transform transition-all duration-300 hover:scale-110 hover:rotate-6">
                  <RefreshCw className="w-6 h-6 text-white" />
                </div>
                <CardTitle className="text-xl">Real-time Sync</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base">
                  Changes sync instantly across all your devices. Never lose track of
                  your tasks, no matter where you are.
                </CardDescription>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="py-20 md:py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="text-4xl md:text-5xl font-bold text-center mb-4 animate-fade-in-up">How It Works</h2>
          <p className="text-xl text-gray-600 text-center mb-16 max-w-3xl mx-auto animate-fade-in-up animation-delay-200">
            Get started in minutes with our simple, straightforward process
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {/* Step 1 */}
            <div className="text-center animate-fade-in-up animation-delay-200 group">
              <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-500 rounded-full flex items-center justify-center mx-auto mb-4 shadow-lg transform transition-all duration-500 group-hover:scale-125 group-hover:rotate-12 animate-float">
                <span className="text-2xl font-bold text-white">1</span>
              </div>
              <h3 className="text-xl font-semibold mb-2 transition-colors duration-300 group-hover:text-blue-600">Sign Up Free</h3>
              <p className="text-gray-600">
                Create your account in seconds. No credit card required, no commitments.
              </p>
            </div>

            {/* Step 2 */}
            <div className="text-center animate-fade-in-up animation-delay-400 group">
              <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-4 shadow-lg transform transition-all duration-500 group-hover:scale-125 group-hover:rotate-12 animate-float animation-delay-200">
                <span className="text-2xl font-bold text-white">2</span>
              </div>
              <h3 className="text-xl font-semibold mb-2 transition-colors duration-300 group-hover:text-purple-600">Add Your Tasks</h3>
              <p className="text-gray-600">
                Quickly add tasks with titles and optional descriptions. Simple and intuitive.
              </p>
            </div>

            {/* Step 3 */}
            <div className="text-center animate-fade-in-up animation-delay-600 group">
              <div className="w-16 h-16 bg-gradient-to-br from-pink-500 to-red-500 rounded-full flex items-center justify-center mx-auto mb-4 shadow-lg transform transition-all duration-500 group-hover:scale-125 group-hover:rotate-12 animate-float animation-delay-400">
                <span className="text-2xl font-bold text-white">3</span>
              </div>
              <h3 className="text-xl font-semibold mb-2 transition-colors duration-300 group-hover:text-pink-600">Stay Organized</h3>
              <p className="text-gray-600">
                Filter, edit, and manage your tasks with powerful organization tools.
              </p>
            </div>

            {/* Step 4 */}
            <div className="text-center animate-fade-in-up animation-delay-800 group">
              <div className="w-16 h-16 bg-gradient-to-br from-red-500 to-orange-500 rounded-full flex items-center justify-center mx-auto mb-4 shadow-lg transform transition-all duration-500 group-hover:scale-125 group-hover:rotate-12 animate-float animation-delay-600">
                <span className="text-2xl font-bold text-white">4</span>
              </div>
              <h3 className="text-xl font-semibold mb-2 transition-colors duration-300 group-hover:text-red-600">Get Things Done</h3>
              <p className="text-gray-600">
                Check off completed tasks and boost your productivity every day.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-20 md:py-24 bg-gradient-to-br from-blue-50 to-purple-50">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="text-4xl md:text-5xl font-bold text-center mb-4 animate-fade-in-up">
            Loved by Thousands of Users
          </h2>
          <p className="text-xl text-gray-600 text-center mb-16 max-w-3xl mx-auto animate-fade-in-up animation-delay-200">
            See what our users have to say about TaskFlow
          </p>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Testimonial 1 */}
            <Card className="p-6 hover:shadow-xl transition-all duration-500 hover:-translate-y-2 animate-fade-in-up animation-delay-200 hover:border-blue-300 border-2 border-transparent">
              <div className="flex items-center mb-4">
                <div className="flex text-yellow-400 text-xl">
                  ★★★★★
                </div>
              </div>
              <p className="text-gray-700 mb-4 leading-relaxed">
                "This app has completely transformed how I manage my daily tasks.
                Simple, fast, and exactly what I needed!"
              </p>
              <div className="flex items-center">
                <div className="w-10 h-10 bg-gradient-to-br from-blue-400 to-purple-400 rounded-full mr-3 animate-pulse"></div>
                <div>
                  <div className="font-semibold">Sarah Johnson</div>
                  <div className="text-sm text-gray-500">Product Manager</div>
                </div>
              </div>
            </Card>

            {/* Testimonial 2 */}
            <Card className="p-6 hover:shadow-xl transition-all duration-500 hover:-translate-y-2 animate-fade-in-up animation-delay-400 hover:border-purple-300 border-2 border-transparent">
              <div className="flex items-center mb-4">
                <div className="flex text-yellow-400 text-xl">
                  ★★★★★
                </div>
              </div>
              <p className="text-gray-700 mb-4 leading-relaxed">
                "Finally, a todo app that doesn't overcomplicate things.
                Clean interface and powerful features."
              </p>
              <div className="flex items-center">
                <div className="w-10 h-10 bg-gradient-to-br from-purple-400 to-pink-400 rounded-full mr-3 animate-pulse animation-delay-200"></div>
                <div>
                  <div className="font-semibold">Michael Chen</div>
                  <div className="text-sm text-gray-500">Software Engineer</div>
                </div>
              </div>
            </Card>

            {/* Testimonial 3 */}
            <Card className="p-6 hover:shadow-xl transition-all duration-500 hover:-translate-y-2 animate-fade-in-up animation-delay-600 hover:border-pink-300 border-2 border-transparent">
              <div className="flex items-center mb-4">
                <div className="flex text-yellow-400 text-xl">
                  ★★★★★
                </div>
              </div>
              <p className="text-gray-700 mb-4 leading-relaxed">
                "I've tried many todo apps, but this one stands out.
                The security and privacy features give me peace of mind."
              </p>
              <div className="flex items-center">
                <div className="w-10 h-10 bg-gradient-to-br from-pink-400 to-red-400 rounded-full mr-3 animate-pulse animation-delay-400"></div>
                <div>
                  <div className="font-semibold">Emily Rodriguez</div>
                  <div className="text-sm text-gray-500">Freelance Designer</div>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-20 md:py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="text-4xl md:text-5xl font-bold text-center mb-4 animate-fade-in-up">
            Simple, Transparent Pricing
          </h2>
          <p className="text-xl text-gray-600 text-center mb-16 max-w-3xl mx-auto animate-fade-in-up animation-delay-200">
            Start free, upgrade when you need more. No hidden fees, cancel anytime.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {/* Free Plan */}
            <Card className="border-2 p-8 hover:shadow-xl transition-all duration-500 hover:-translate-y-2 animate-fade-in-up animation-delay-200 hover:border-blue-300">
              <h3 className="text-2xl font-bold mb-2">Free</h3>
              <div className="text-5xl font-bold mb-4">
                $0<span className="text-lg text-gray-500 font-normal">/month</span>
              </div>
              <p className="text-gray-600 mb-6">Perfect for personal use</p>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center transform transition-all duration-300 hover:translate-x-2">
                  <CheckCircle2 className="w-5 h-5 text-green-500 mr-2 flex-shrink-0" />
                  <span>Unlimited tasks</span>
                </li>
                <li className="flex items-center transform transition-all duration-300 hover:translate-x-2">
                  <CheckCircle2 className="w-5 h-5 text-green-500 mr-2 flex-shrink-0" />
                  <span>Basic filters</span>
                </li>
                <li className="flex items-center transform transition-all duration-300 hover:translate-x-2">
                  <CheckCircle2 className="w-5 h-5 text-green-500 mr-2 flex-shrink-0" />
                  <span>Mobile access</span>
                </li>
                <li className="flex items-center transform transition-all duration-300 hover:translate-x-2">
                  <CheckCircle2 className="w-5 h-5 text-green-500 mr-2 flex-shrink-0" />
                  <span>Secure encryption</span>
                </li>
              </ul>
              <Link href="/signup">
                <Button className="w-full transition-all duration-300 hover:scale-105 hover:shadow-lg" variant="outline" size="lg">
                  Get Started
                </Button>
              </Link>
            </Card>

            {/* Pro Plan */}
            <Card className="border-4 border-blue-500 p-8 relative hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-4 animate-fade-in-up animation-delay-400 hover:border-purple-500">
              <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                <span className="bg-gradient-to-r from-blue-500 to-purple-500 text-white px-4 py-1 rounded-full text-sm font-semibold shadow-lg animate-pulse">
                  Most Popular
                </span>
              </div>
              <h3 className="text-2xl font-bold mb-2">Pro</h3>
              <div className="text-5xl font-bold mb-4">
                $9<span className="text-lg text-gray-500 font-normal">/month</span>
              </div>
              <p className="text-gray-600 mb-6">For power users</p>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center transform transition-all duration-300 hover:translate-x-2">
                  <CheckCircle2 className="w-5 h-5 text-green-500 mr-2 flex-shrink-0" />
                  <span>Everything in Free</span>
                </li>
                <li className="flex items-center transform transition-all duration-300 hover:translate-x-2">
                  <CheckCircle2 className="w-5 h-5 text-green-500 mr-2 flex-shrink-0" />
                  <span>Advanced filters</span>
                </li>
                <li className="flex items-center transform transition-all duration-300 hover:translate-x-2">
                  <CheckCircle2 className="w-5 h-5 text-green-500 mr-2 flex-shrink-0" />
                  <span>Priority support</span>
                </li>
                <li className="flex items-center transform transition-all duration-300 hover:translate-x-2">
                  <CheckCircle2 className="w-5 h-5 text-green-500 mr-2 flex-shrink-0" />
                  <span>Custom themes</span>
                </li>
                <li className="flex items-center transform transition-all duration-300 hover:translate-x-2">
                  <CheckCircle2 className="w-5 h-5 text-green-500 mr-2 flex-shrink-0" />
                  <span>Export data</span>
                </li>
              </ul>
              <Button className="w-full bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 transition-all duration-300 hover:scale-105 hover:shadow-lg" size="lg">
                Upgrade to Pro
              </Button>
            </Card>

            {/* Team Plan */}
            <Card className="border-2 p-8 hover:shadow-xl transition-all duration-500 hover:-translate-y-2 animate-fade-in-up animation-delay-600 hover:border-orange-300">
              <h3 className="text-2xl font-bold mb-2">Team</h3>
              <div className="text-5xl font-bold mb-4">
                $29<span className="text-lg text-gray-500 font-normal">/month</span>
              </div>
              <p className="text-gray-600 mb-6">For teams & collaboration</p>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center transform transition-all duration-300 hover:translate-x-2">
                  <CheckCircle2 className="w-5 h-5 text-green-500 mr-2 flex-shrink-0" />
                  <span>Everything in Pro</span>
                </li>
                <li className="flex items-center transform transition-all duration-300 hover:translate-x-2">
                  <CheckCircle2 className="w-5 h-5 text-green-500 mr-2 flex-shrink-0" />
                  <span>Up to 10 users</span>
                </li>
                <li className="flex items-center transform transition-all duration-300 hover:translate-x-2">
                  <CheckCircle2 className="w-5 h-5 text-green-500 mr-2 flex-shrink-0" />
                  <span>Shared workspaces</span>
                </li>
                <li className="flex items-center transform transition-all duration-300 hover:translate-x-2">
                  <CheckCircle2 className="w-5 h-5 text-green-500 mr-2 flex-shrink-0" />
                  <span>Team analytics</span>
                </li>
                <li className="flex items-center transform transition-all duration-300 hover:translate-x-2">
                  <CheckCircle2 className="w-5 h-5 text-green-500 mr-2 flex-shrink-0" />
                  <span>Admin controls</span>
                </li>
              </ul>
              <Button className="w-full transition-all duration-300 hover:scale-105 hover:shadow-lg" variant="outline" size="lg">
                Contact Sales
              </Button>
            </Card>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section id="faq" className="py-20 md:py-24 bg-gray-50">
        <div className="max-w-4xl mx-auto px-4">
          <h2 className="text-4xl md:text-5xl font-bold text-center mb-4 animate-fade-in-up">
            Frequently Asked Questions
          </h2>
          <p className="text-xl text-gray-600 text-center mb-16 animate-fade-in-up animation-delay-200">
            Everything you need to know about TaskFlow
          </p>

          <div className="space-y-6">
            {/* FAQ Item 1 */}
            <Card className="p-6 hover:shadow-lg transition-all duration-300 hover:-translate-y-1 animate-fade-in-up animation-delay-200 hover:border-blue-300 border-2 border-transparent">
              <h3 className="text-xl font-semibold mb-2">
                Is the free plan really free forever?
              </h3>
              <p className="text-gray-600 leading-relaxed">
                Yes! Our free plan includes unlimited tasks and core features with no time limit.
                You can upgrade to Pro anytime for advanced features, but the free plan will always be available.
              </p>
            </Card>

            {/* FAQ Item 2 */}
            <Card className="p-6 hover:shadow-lg transition-all duration-300 hover:-translate-y-1 animate-fade-in-up animation-delay-400 hover:border-purple-300 border-2 border-transparent">
              <h3 className="text-xl font-semibold mb-2">
                How secure is my data?
              </h3>
              <p className="text-gray-600 leading-relaxed">
                We use industry-standard encryption and JWT authentication to protect your data.
                Your tasks are stored securely in our database and only accessible by you. We never share your data with third parties.
              </p>
            </Card>

            {/* FAQ Item 3 */}
            <Card className="p-6 hover:shadow-lg transition-all duration-300 hover:-translate-y-1 animate-fade-in-up animation-delay-600 hover:border-pink-300 border-2 border-transparent">
              <h3 className="text-xl font-semibold mb-2">
                Can I access my tasks on mobile?
              </h3>
              <p className="text-gray-600 leading-relaxed">
                Yes! Our web app is fully responsive and works perfectly on all devices - smartphones, tablets, and desktops.
                Native mobile apps for iOS and Android are coming soon.
              </p>
            </Card>

            {/* FAQ Item 4 */}
            <Card className="p-6 hover:shadow-lg transition-all duration-300 hover:-translate-y-1 animate-fade-in-up animation-delay-800 hover:border-green-300 border-2 border-transparent">
              <h3 className="text-xl font-semibold mb-2">
                Can I export my data?
              </h3>
              <p className="text-gray-600 leading-relaxed">
                Pro and Team users can export their tasks in JSON or CSV format at any time.
                We believe your data should always be portable and accessible to you.
              </p>
            </Card>

            {/* FAQ Item 5 */}
            <Card className="p-6 hover:shadow-lg transition-all duration-300 hover:-translate-y-1 animate-fade-in-up animation-delay-1000 hover:border-orange-300 border-2 border-transparent">
              <h3 className="text-xl font-semibold mb-2">
                Do you offer refunds?
              </h3>
              <p className="text-gray-600 leading-relaxed">
                Yes! We offer a 30-day money-back guarantee on all paid plans.
                If you're not satisfied for any reason, contact us and we'll refund you in full, no questions asked.
              </p>
            </Card>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-300">
        <div className="max-w-7xl mx-auto px-4 py-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
            {/* Brand Column */}
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-500 rounded-lg flex items-center justify-center">
                  <CheckCircle2 className="w-5 h-5 text-white" />
                </div>
                <h3 className="text-white font-bold text-xl">TaskFlow</h3>
              </div>
              <p className="text-sm leading-relaxed">
                The simple, powerful todo app for staying organized and productive.
              </p>
            </div>

            {/* Product Column */}
            <div>
              <h4 className="text-white font-semibold mb-4">Product</h4>
              <ul className="space-y-2 text-sm">
                <li>
                  <button onClick={() => document.getElementById('features')?.scrollIntoView({ behavior: 'smooth' })} className="hover:text-white transition-colors">
                    Features
                  </button>
                </li>
                <li>
                  <button onClick={() => document.getElementById('pricing')?.scrollIntoView({ behavior: 'smooth' })} className="hover:text-white transition-colors">
                    Pricing
                  </button>
                </li>
                <li>
                  <button onClick={() => document.getElementById('faq')?.scrollIntoView({ behavior: 'smooth' })} className="hover:text-white transition-colors">
                    FAQ
                  </button>
                </li>
              </ul>
            </div>

            {/* Company Column */}
            <div>
              <h4 className="text-white font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-sm">
                <li><Link href="#" className="hover:text-white transition-colors">About</Link></li>
                <li><Link href="#" className="hover:text-white transition-colors">Blog</Link></li>
                <li><Link href="#" className="hover:text-white transition-colors">Contact</Link></li>
              </ul>
            </div>

            {/* Legal Column */}
            <div>
              <h4 className="text-white font-semibold mb-4">Legal</h4>
              <ul className="space-y-2 text-sm">
                <li><Link href="#" className="hover:text-white transition-colors">Privacy</Link></li>
                <li><Link href="#" className="hover:text-white transition-colors">Terms</Link></li>
                <li><Link href="#" className="hover:text-white transition-colors">Security</Link></li>
              </ul>
            </div>
          </div>

          <div className="border-t border-gray-800 pt-8 text-center text-sm">
            <p>© {new Date().getFullYear()} TaskFlow. All rights reserved.</p>
            <p className="mt-2 text-gray-500">
              Built with Next.js, FastAPI, and PostgreSQL
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
