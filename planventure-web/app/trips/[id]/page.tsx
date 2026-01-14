'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import Link from 'next/link';
import api from '@/lib/api';

interface ItineraryItem {
  id: number;
  day: number;
  title: string;
  location?: string;
  description?: string;
  start_time?: string;
  end_time?: string;
}

interface Expense {
  id: number;
  category: string;
  description?: string;
  amount: number;
  currency: string;
}

interface Trip {
  id: number;
  title: string;
  destination: string;
  description?: string;
  start_date?: string;
  end_date?: string;
}

export default function TripPage() {
  const router = useRouter();
  const params = useParams();
  const tripId = parseInt(params.id as string);

  const [trip, setTrip] = useState<Trip | null>(null);
  const [itinerary, setItinerary] = useState<ItineraryItem[]>([]);
  const [expenses, setExpenses] = useState<Expense[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAddItem, setShowAddItem] = useState(false);
  const [newItem, setNewItem] = useState({
    day: 1,
    title: '',
    location: '',
    description: '',
  });

  useEffect(() => {
    fetchTripData();
  }, [tripId]);

  const fetchTripData = async () => {
    try {
      const [tripRes, itineraryRes, expensesRes] = await Promise.all([
        api.get(`/trips/${tripId}`),
        api.get(`/trips/${tripId}/itinerary`),
        api.get(`/trips/${tripId}/expenses`),
      ]);

      setTrip(tripRes.data);
      setItinerary(itineraryRes.data);
      setExpenses(expensesRes.data);
    } catch (error) {
      console.error('Failed to fetch trip data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddItem = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post(`/trips/${tripId}/itinerary`, newItem);
      setNewItem({ day: 1, title: '', location: '', description: '' });
      setShowAddItem(false);
      fetchTripData();
    } catch (error) {
      console.error('Failed to add itinerary item:', error);
    }
  };

  const totalExpenses = expenses.reduce((sum, exp) => sum + exp.amount, 0);

  if (loading) return <div className="text-center py-12">Loading trip...</div>;
  if (!trip) return <div className="text-center py-12">Trip not found</div>;

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-4xl mx-auto">
        <Link href="/dashboard" className="text-blue-600 hover:underline mb-6 inline-block">
          ← Back to Dashboard
        </Link>

        {/* Trip Header */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">{trip.title}</h1>
          <p className="text-2xl text-gray-600 mb-4">{trip.destination}</p>
          {trip.description && <p className="text-gray-700 mb-4">{trip.description}</p>}
          {trip.start_date && (
            <p className="text-gray-600">
              {new Date(trip.start_date).toLocaleDateString()} - {new Date(trip.end_date || trip.start_date).toLocaleDateString()}
            </p>
          )}
        </div>

        {/* Expenses Summary */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Expenses</h2>
          <div className="mb-4">
            <p className="text-3xl font-bold text-blue-600">${totalExpenses.toFixed(2)}</p>
            <p className="text-gray-600">{expenses.length} expenses</p>
          </div>
          {expenses.length > 0 && (
            <div className="space-y-2">
              {expenses.map((expense) => (
                <div key={expense.id} className="flex justify-between p-2 bg-gray-50 rounded">
                  <span>{expense.description || expense.category}</span>
                  <span className="font-semibold">${expense.amount.toFixed(2)}</span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Itinerary */}
        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900">Itinerary</h2>
            <button
              onClick={() => setShowAddItem(!showAddItem)}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
            >
              + Add Activity
            </button>
          </div>

          {showAddItem && (
            <form onSubmit={handleAddItem} className="mb-6 p-4 bg-gray-50 rounded-lg">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <input
                  type="number"
                  placeholder="Day"
                  value={newItem.day}
                  onChange={(e) => setNewItem({ ...newItem, day: parseInt(e.target.value) })}
                  className="px-3 py-2 border border-gray-300 rounded-lg"
                  min="1"
                  required
                />
                <input
                  type="text"
                  placeholder="Title"
                  value={newItem.title}
                  onChange={(e) => setNewItem({ ...newItem, title: e.target.value })}
                  className="px-3 py-2 border border-gray-300 rounded-lg"
                  required
                />
                <input
                  type="text"
                  placeholder="Location"
                  value={newItem.location}
                  onChange={(e) => setNewItem({ ...newItem, location: e.target.value })}
                  className="px-3 py-2 border border-gray-300 rounded-lg"
                />
                <input
                  type="text"
                  placeholder="Description"
                  value={newItem.description}
                  onChange={(e) => setNewItem({ ...newItem, description: e.target.value })}
                  className="px-3 py-2 border border-gray-300 rounded-lg"
                />
              </div>
              <div className="flex gap-2 mt-4">
                <button
                  type="submit"
                  className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700"
                >
                  Add
                </button>
                <button
                  type="button"
                  onClick={() => setShowAddItem(false)}
                  className="bg-gray-400 text-white px-4 py-2 rounded-lg hover:bg-gray-500"
                >
                  Cancel
                </button>
              </div>
            </form>
          )}

          {itinerary.length === 0 ? (
            <p className="text-gray-600">No itinerary items yet</p>
          ) : (
            <div className="space-y-4">
              {itinerary
                .sort((a, b) => a.day - b.day)
                .map((item) => (
                  <div key={item.id} className="border-l-4 border-blue-600 pl-4 py-2">
                    <div className="flex justify-between items-start">
                      <div>
                        <h3 className="font-bold text-lg">{item.title}</h3>
                        <p className="text-gray-600">Day {item.day}</p>
                        {item.location && <p className="text-gray-600">{item.location}</p>}
                        {item.description && <p className="text-gray-700 mt-1">{item.description}</p>}
                        {item.start_time && (
                          <p className="text-sm text-gray-500">
                            {item.start_time} - {item.end_time || ''}
                          </p>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
