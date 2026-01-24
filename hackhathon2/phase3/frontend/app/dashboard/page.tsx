"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { useAuth } from "@/components/auth/AuthContext";
import { LogOut, User, Mail, Calendar, Loader2, CheckCircle2, Circle, Edit2, Trash2, Plus } from "lucide-react";
import apiClient from "@/lib/api-client";
import type { Task } from "@/types/task";
import { ChatButton } from "@/components/ChatButton";
import { ChatInterface } from "@/components/ChatInterface";

export default function DashboardPage() {
  const router = useRouter();
  const { user, isLoading, isAuthenticated, logout } = useAuth();

  // Todo state
  const [todos, setTodos] = useState<Task[]>([]);
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');
  const [isLoadingTodos, setIsLoadingTodos] = useState(true);

  // Form state
  const [newTodo, setNewTodo] = useState({ title: '', description: '' });
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editForm, setEditForm] = useState({ title: '', description: '', completed: false });

  // UI state
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string>('');
  const [isChatOpen, setIsChatOpen] = useState(false);

  // Redirect to signin if not authenticated
  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push("/signin");
    }
  }, [isLoading, isAuthenticated, router]);

  // Fetch todos on mount
  useEffect(() => {
    if (user?.id) {
      fetchTodos();
    }
  }, [user?.id]);

  // Fetch todos from API
  const fetchTodos = async () => {
    try {
      setIsLoadingTodos(true);
      const response = await apiClient.get(`/api/users/${user?.id}/tasks`);
      setTodos(response.data);
      setError('');
    } catch (err: any) {
      console.error('Error fetching todos:', err);
      setError('Failed to load todos');
    } finally {
      setIsLoadingTodos(false);
    }
  };

  // Create new todo
  const handleCreateTodo = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTodo.title.trim()) return;

    try {
      setIsSubmitting(true);
      await apiClient.post(`/api/users/${user?.id}/tasks`, {
        title: newTodo.title,
        description: newTodo.description || undefined,
      });
      setNewTodo({ title: '', description: '' });
      await fetchTodos();
      setError('');
    } catch (err: any) {
      console.error('Error creating todo:', err);
      setError(err.response?.data?.detail || 'Failed to create todo');
    } finally {
      setIsSubmitting(false);
    }
  };

  // Toggle todo completion
  const handleToggleTodo = async (taskId: string) => {
    try {
      await apiClient.patch(`/api/users/${user?.id}/tasks/${taskId}/toggle`);
      await fetchTodos();
      setError('');
    } catch (err: any) {
      console.error('Error toggling todo:', err);
      setError('Failed to update todo');
    }
  };

  // Start editing a todo
  const startEdit = (todo: Task) => {
    setEditingId(todo.id);
    setEditForm({
      title: todo.title,
      description: todo.description || '',
      completed: todo.completed,
    });
  };

  // Save edited todo
  const handleUpdateTodo = async (taskId: string) => {
    if (!editForm.title.trim()) return;

    try {
      setIsSubmitting(true);
      await apiClient.put(`/api/users/${user?.id}/tasks/${taskId}`, {
        title: editForm.title,
        description: editForm.description || undefined,
        completed: editForm.completed,
      });
      setEditingId(null);
      await fetchTodos();
      setError('');
    } catch (err: any) {
      console.error('Error updating todo:', err);
      setError(err.response?.data?.detail || 'Failed to update todo');
    } finally {
      setIsSubmitting(false);
    }
  };

  // Delete todo
  const handleDeleteTodo = async (taskId: string) => {
    if (!confirm('Are you sure you want to delete this todo?')) return;

    try {
      await apiClient.delete(`/api/users/${user?.id}/tasks/${taskId}`);
      await fetchTodos();
      setError('');
    } catch (err: any) {
      console.error('Error deleting todo:', err);
      setError('Failed to delete todo');
    }
  };

  // Filter todos
  const filteredTodos = todos.filter(todo => {
    if (filter === 'active') return !todo.completed;
    if (filter === 'completed') return todo.completed;
    return true;
  });

  // Calculate stats
  const stats = {
    total: todos.length,
    active: todos.filter(t => !t.completed).length,
    completed: todos.filter(t => t.completed).length,
  };

  // Handle logout
  const handleLogout = () => {
    logout();
    router.push("/");
  };

  // Show loading state
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <Loader2 className="w-8 h-8 animate-spin mx-auto text-blue-600" />
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  // Don't render if not authenticated (will redirect)
  if (!isAuthenticated || !user) {
    return null;
  }

  // Format date
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-gray-900 animate-fade-in">Dashboard</h1>
            <Button
              onClick={handleLogout}
              variant="outline"
              className="flex items-center gap-2 transition-all duration-300 hover:scale-105 hover:shadow-md"
            >
              <LogOut className="w-4 h-4" />
              Logout
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="mb-8 animate-fade-in-up">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            Welcome back{user.name ? `, ${user.name}` : ""}!
          </h2>
          <p className="text-gray-600">
            Here's your account information and activity overview.
          </p>
        </div>

        {/* User Information Card */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <Card className="animate-fade-in-up animation-delay-200 hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <User className="w-5 h-5 text-blue-600" />
                Account Information
              </CardTitle>
              <CardDescription>Your personal details</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-start gap-3">
                <Mail className="w-5 h-5 text-gray-400 mt-0.5" />
                <div>
                  <p className="text-sm font-medium text-gray-500">Email</p>
                  <p className="text-base text-gray-900">{user.email}</p>
                </div>
              </div>

              {user.name && (
                <div className="flex items-start gap-3">
                  <User className="w-5 h-5 text-gray-400 mt-0.5" />
                  <div>
                    <p className="text-sm font-medium text-gray-500">Name</p>
                    <p className="text-base text-gray-900">{user.name}</p>
                  </div>
                </div>
              )}

              <div className="flex items-start gap-3">
                <Calendar className="w-5 h-5 text-gray-400 mt-0.5" />
                <div>
                  <p className="text-sm font-medium text-gray-500">Member Since</p>
                  <p className="text-base text-gray-900">{formatDate(user.created_at)}</p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <User className="w-5 h-5 text-gray-400 mt-0.5" />
                <div>
                  <p className="text-sm font-medium text-gray-500">User ID</p>
                  <p className="text-xs text-gray-600 font-mono">{user.id}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Quick Stats Card */}
          <Card className="animate-fade-in-up animation-delay-400 hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
            <CardHeader>
              <CardTitle>Quick Stats</CardTitle>
              <CardDescription>Your activity at a glance</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex justify-between items-center p-4 bg-blue-50 rounded-lg transition-all duration-300 hover:bg-blue-100 hover:scale-105">
                <div>
                  <p className="text-sm font-medium text-gray-600">Account Status</p>
                  <p className="text-lg font-semibold text-blue-600">Active</p>
                </div>
                <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                  <User className="w-6 h-6 text-blue-600" />
                </div>
              </div>

              <div className="flex justify-between items-center p-4 bg-green-50 rounded-lg transition-all duration-300 hover:bg-green-100 hover:scale-105">
                <div>
                  <p className="text-sm font-medium text-gray-600">Authentication</p>
                  <p className="text-lg font-semibold text-green-600">Verified</p>
                </div>
                <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                  <svg
                    className="w-6 h-6 text-green-600"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                </div>
              </div>

              <div className="flex justify-between items-center p-4 bg-purple-50 rounded-lg transition-all duration-300 hover:bg-purple-100 hover:scale-105">
                <div>
                  <p className="text-sm font-medium text-gray-600">Total Tasks</p>
                  <p className="text-lg font-semibold text-purple-600">{stats.total}</p>
                </div>
                <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center">
                  <CheckCircle2 className="w-6 h-6 text-purple-600" />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Todo Management Section */}
        <Card className="animate-fade-in-up animation-delay-600 hover:shadow-xl transition-shadow duration-300">
          <CardHeader>
            <CardTitle>My Todos</CardTitle>
            <CardDescription>Manage your tasks and stay organized</CardDescription>

            {/* Filter Tabs */}
            <div className="flex gap-2 mt-4">
              <Button
                size="sm"
                variant={filter === 'all' ? 'default' : 'outline'}
                onClick={() => setFilter('all')}
                className="transition-all duration-300 hover:scale-105"
              >
                All ({stats.total})
              </Button>
              <Button
                size="sm"
                variant={filter === 'active' ? 'default' : 'outline'}
                onClick={() => setFilter('active')}
                className="transition-all duration-300 hover:scale-105"
              >
                Active ({stats.active})
              </Button>
              <Button
                size="sm"
                variant={filter === 'completed' ? 'default' : 'outline'}
                onClick={() => setFilter('completed')}
                className="transition-all duration-300 hover:scale-105"
              >
                Completed ({stats.completed})
              </Button>
            </div>
          </CardHeader>

          <CardContent>
            {/* Error Message */}
            {error && (
              <div className="mb-4 p-3 text-sm text-red-800 bg-red-50 border border-red-200 rounded-md animate-shake">
                {error}
              </div>
            )}

            {/* Add Todo Form */}
            <form onSubmit={handleCreateTodo} className="space-y-3 mb-6 p-4 bg-gradient-to-br from-blue-50 to-purple-50 rounded-lg border border-blue-100 shadow-sm">
              <Input
                placeholder="What needs to be done?"
                value={newTodo.title}
                onChange={(e) => setNewTodo({ ...newTodo, title: e.target.value })}
                disabled={isSubmitting}
                className="bg-white transition-all duration-300 focus:scale-105"
              />
              <Input
                placeholder="Description (optional)"
                value={newTodo.description}
                onChange={(e) => setNewTodo({ ...newTodo, description: e.target.value })}
                disabled={isSubmitting}
                className="bg-white transition-all duration-300 focus:scale-105"
              />
              <Button
                type="submit"
                disabled={!newTodo.title.trim() || isSubmitting}
                className="w-full transition-all duration-300 hover:scale-105 hover:shadow-lg"
              >
                {isSubmitting ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Adding...
                  </>
                ) : (
                  <>
                    <Plus className="w-4 h-4 mr-2" />
                    Add Todo
                  </>
                )}
              </Button>
            </form>

            {/* Todo List */}
            {isLoadingTodos ? (
              <div className="text-center py-8">
                <Loader2 className="w-8 h-8 animate-spin mx-auto text-blue-600" />
                <p className="mt-2 text-gray-600">Loading todos...</p>
              </div>
            ) : filteredTodos.length === 0 ? (
              <div className="text-center py-8">
                <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  {filter === 'completed' ? (
                    <CheckCircle2 className="w-8 h-8 text-gray-400" />
                  ) : (
                    <Circle className="w-8 h-8 text-gray-400" />
                  )}
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {filter === 'all' && 'No todos yet'}
                  {filter === 'active' && 'No active todos'}
                  {filter === 'completed' && 'No completed todos'}
                </h3>
                <p className="text-gray-600">
                  {filter === 'all' && 'Create your first todo to get started!'}
                  {filter === 'active' && 'All your todos are completed!'}
                  {filter === 'completed' && 'Complete some todos to see them here.'}
                </p>
              </div>
            ) : (
              <div className="space-y-2">
                {filteredTodos.map((todo) => (
                  <div
                    key={todo.id}
                    className="flex items-start gap-3 p-3 border rounded-lg hover:bg-gradient-to-r hover:from-blue-50 hover:to-purple-50 transition-all duration-300 hover:shadow-md hover:-translate-y-0.5 animate-fade-in"
                  >
                    {/* Checkbox */}
                    <button
                      onClick={() => handleToggleTodo(todo.id)}
                      className="mt-0.5 flex-shrink-0"
                      disabled={editingId === todo.id}
                    >
                      {todo.completed ? (
                        <CheckCircle2 className="w-5 h-5 text-green-600" />
                      ) : (
                        <Circle className="w-5 h-5 text-gray-400 hover:text-gray-600" />
                      )}
                    </button>

                    {/* Content */}
                    {editingId === todo.id ? (
                      <div className="flex-1 space-y-2">
                        <Input
                          value={editForm.title}
                          onChange={(e) => setEditForm({ ...editForm, title: e.target.value })}
                          disabled={isSubmitting}
                          placeholder="Title"
                        />
                        <Input
                          value={editForm.description}
                          onChange={(e) => setEditForm({ ...editForm, description: e.target.value })}
                          disabled={isSubmitting}
                          placeholder="Description (optional)"
                        />
                        <div className="flex gap-2">
                          <Button
                            size="sm"
                            onClick={() => handleUpdateTodo(todo.id)}
                            disabled={!editForm.title.trim() || isSubmitting}
                          >
                            {isSubmitting ? (
                              <>
                                <Loader2 className="w-3 h-3 mr-1 animate-spin" />
                                Saving...
                              </>
                            ) : (
                              'Save'
                            )}
                          </Button>
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => setEditingId(null)}
                            disabled={isSubmitting}
                          >
                            Cancel
                          </Button>
                        </div>
                      </div>
                    ) : (
                      <div className="flex-1 min-w-0">
                        <p className={`font-medium ${todo.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                          {todo.title}
                        </p>
                        {todo.description && (
                          <p className={`text-sm mt-1 ${todo.completed ? 'line-through text-gray-400' : 'text-gray-600'}`}>
                            {todo.description}
                          </p>
                        )}
                        <p className="text-xs text-gray-400 mt-1">
                          {new Date(todo.created_at).toLocaleDateString('en-US', {
                            month: 'short',
                            day: 'numeric',
                            year: 'numeric',
                          })}
                        </p>
                      </div>
                    )}

                    {/* Actions */}
                    {editingId !== todo.id && (
                      <div className="flex gap-1 flex-shrink-0">
                        <Button
                          size="sm"
                          variant="ghost"
                          onClick={() => startEdit(todo)}
                          className="h-8 w-8 p-0"
                        >
                          <Edit2 className="w-4 h-4" />
                        </Button>
                        <Button
                          size="sm"
                          variant="ghost"
                          onClick={() => handleDeleteTodo(todo.id)}
                          className="h-8 w-8 p-0 text-red-600 hover:text-red-700 hover:bg-red-50"
                        >
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </main>

      {/* Phase 3: AI Chat Interface */}
      <ChatButton onClick={() => setIsChatOpen(!isChatOpen)} isOpen={isChatOpen} />
      <ChatInterface isOpen={isChatOpen} onClose={() => setIsChatOpen(false)} />
    </div>
  );
}
