'use client';

import { useState } from 'react';
import { Loader2 } from 'lucide-react';

import { Scenario } from '@/lib/api';

interface ScenarioInputProps {
  onScenarioCreated: (scenario: Scenario) => void;
}

export default function ScenarioInput({ onScenarioCreated }: ScenarioInputProps) {
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!description.trim()) {
      setError('Please enter a scenario description');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/scenarios`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ description }),
      });

      if (!response.ok) {
        throw new Error('Failed to create scenario');
      }

      const scenario = await response.json();
      onScenarioCreated(scenario);
      setDescription('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="scenario" className="block text-sm font-medium text-gray-700 mb-2">
            Describe Your Market Scenario
          </label>
          <textarea
            id="scenario"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="e.g., S&P 500 down 5% over the next month, or Fed delays interest rate cuts"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
            rows={4}
            disabled={loading}
          />
        </div>

        {error && (
          <div className="text-red-600 text-sm">{error}</div>
        )}

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-primary-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-primary-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Analyzing Scenario...
            </>
          ) : (
            'Generate Investment Plays'
          )}
        </button>
      </form>
    </div>
  );
}
