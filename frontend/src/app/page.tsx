'use client';

import { useState } from 'react';
import ScenarioInput from '@/components/ScenarioInput';
import PlayCard from '@/components/PlayCard';
import TrackingDashboard from '@/components/TrackingDashboard';
import { Scenario, TrackedScenario, trackingAPI } from '@/lib/api';
import { Activity } from 'lucide-react';

export default function Home() {
  const [currentScenario, setCurrentScenario] = useState<Scenario | null>(null);
  const [trackedScenario, setTrackedScenario] = useState<TrackedScenario | null>(null);
  const [view, setView] = useState<'create' | 'plays' | 'tracking'>('create');
  const [trackingLoading, setTrackingLoading] = useState(false);

  const handleScenarioCreated = (scenario: Scenario) => {
    setCurrentScenario(scenario);
    setView('plays');
  };

  const handleTrackPlay = async (playId: string) => {
    if (!currentScenario) return;

    setTrackingLoading(true);
    try {
      const tracked = await trackingAPI.start(currentScenario.id, playId);
      setTrackedScenario(tracked);
      setView('tracking');
    } catch (error) {
      console.error('Error starting tracking:', error);
      alert('Failed to start tracking. Please try again.');
    } finally {
      setTrackingLoading(false);
    }
  };

  const handleRefresh = async () => {
    if (!trackedScenario) return;

    try {
      const refreshed = await trackingAPI.refresh(
        trackedScenario.scenario.id,
        trackedScenario.play.id
      );
      setTrackedScenario(refreshed);
    } catch (error) {
      console.error('Error refreshing tracked scenario:', error);
      alert('Failed to refresh. Please try again.');
    }
  };

  const handleStopTracking = async () => {
    if (!trackedScenario) return;

    try {
      await trackingAPI.stop(trackedScenario.scenario.id, trackedScenario.play.id);
      setTrackedScenario(null);
      setView('create');
      setCurrentScenario(null);
    } catch (error) {
      console.error('Error stopping tracking:', error);
      alert('Failed to stop tracking. Please try again.');
    }
  };

  const handleBackToCreate = () => {
    setCurrentScenario(null);
    setView('create');
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-primary-600 rounded-lg">
                <Activity className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">Hedge Fund Agent</h1>
                <p className="text-sm text-gray-600">AI-Powered Trading Guidance</p>
              </div>
            </div>
            {view !== 'create' && (
              <button
                onClick={handleBackToCreate}
                className="px-4 py-2 text-primary-600 hover:text-primary-700 font-medium transition-colors"
              >
                ← New Scenario
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-12">
        {view === 'create' && (
          <div className="space-y-8">
            <div className="text-center">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                Discover Investment Opportunities
              </h2>
              <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                Describe a market scenario and get AI-powered investment recommendations 
                across equities, commodities, and fixed income.
              </p>
            </div>
            <ScenarioInput onScenarioCreated={handleScenarioCreated} />
          </div>
        )}

        {view === 'plays' && currentScenario && (
          <div className="space-y-8">
            <div>
              <button
                onClick={handleBackToCreate}
                className="text-primary-600 hover:text-primary-700 mb-4"
              >
                ← Back
              </button>
              <h2 className="text-3xl font-bold text-gray-900 mb-2">
                Investment Plays
              </h2>
              <p className="text-gray-600 mb-4">{currentScenario.description}</p>
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <p className="text-sm font-semibold text-blue-900 mb-1">Analysis:</p>
                <p className="text-sm text-blue-800">{currentScenario.interpreted_scenario}</p>
              </div>
            </div>

            <div className="grid md:grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
              {currentScenario.plays.map((play) => (
                <PlayCard
                  key={play.id}
                  play={play}
                  scenarioId={currentScenario.id}
                  onTrack={handleTrackPlay}
                  isTracking={trackingLoading}
                />
              ))}
            </div>
          </div>
        )}

        {view === 'tracking' && trackedScenario && (
          <TrackingDashboard
            trackedScenario={trackedScenario}
            onRefresh={handleRefresh}
            onStop={handleStopTracking}
          />
        )}
      </div>
    </main>
  );
}
