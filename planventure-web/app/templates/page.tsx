'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuthStore } from '../../lib/store';
import api from '../../lib/api';

interface TripTemplate {
  id: number;
  title: string;
  category: string;
  difficulty: string;
  estimated_budget: number;
  duration_days: number;
  description?: string;
}

export default function TemplatesPage() {
  const router = useRouter();
  const { isAuthenticated, checkAuth } = useAuthStore();
  const [templates, setTemplates] = useState<TripTemplate[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }

    fetchTemplates();
  }, [isAuthenticated, router]);

  const fetchTemplates = async () => {
    try {
      const response = await api.get('/templates');
      setTemplates(response.data);
    } catch (error) {
      console.error('Failed to fetch templates:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleUseTemplate = async (templateId: number) => {
    try {
      const response = await api.post(`/templates/${templateId}/use`);
      router.push(`/trips/${response.data.id}`);
    } catch (error) {
      console.error('Failed to use template:', error);
      alert('Failed to create trip from template.');
    }
  };

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 flex justify-between items-center">
          <Link href="/dashboard" className="text-3xl font-bold text-gray-900 hover:text-blue-600">
            PlanVenture
          </Link>
          <Link
            href="/dashboard"
            className="text-blue-600 hover:underline"
          >
            Back to Dashboard
          </Link>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Trip Templates</h1>
          <p className="text-gray-600">Choose from pre-made trip templates to get started quickly.</p>
        </div>

        {loading ? (
          <div className="text-center py-12">Loading templates...</div>
        ) : templates.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-lg">
            <p className="text-gray-600">No templates available yet.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {templates.map((template) => (
              <div key={template.id} className="bg-white rounded-lg shadow hover:shadow-lg transition p-6">
                <div className="mb-4">
                  <span className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">
                    {template.category}
                  </span>
                  <span className={`inline-block ml-2 text-xs px-2 py-1 rounded-full ${
                    template.difficulty === 'easy' ? 'bg-green-100 text-green-800' :
                    template.difficulty === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                  }`}>
                    {template.difficulty}
                  </span>
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">{template.title}</h3>
                {template.description && (
                  <p className="text-gray-600 mb-4 line-clamp-3">{template.description}</p>
                )}
                <div className="mb-4 text-sm text-gray-500">
                  <p>Duration: {template.duration_days} days</p>
                  <p>Budget: ${template.estimated_budget}</p>
                </div>
                <button
                  onClick={() => handleUseTemplate(template.id)}
                  className="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
                >
                  Use Template
                </button>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}