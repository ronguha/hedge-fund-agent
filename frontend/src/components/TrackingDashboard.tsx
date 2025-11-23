'use client';

import { useState, useEffect } from 'react';
import { TrackedScenario } from '@/lib/api';
import { RefreshCw, AlertTriangle, Info, AlertCircle, ExternalLink, TrendingUp } from 'lucide-react';

interface TrackingDashboardProps {
  trackedScenario: TrackedScenario;
  onRefresh: () => void;
  onStop: () => void;
}

export default function TrackingDashboard({ trackedScenario, onRefresh, onStop }: TrackingDashboardProps) {
  const [refreshing, setRefreshing] = useState(false);

  const handleRefresh = async () => {
    setRefreshing(true);
    await onRefresh();
    setRefreshing(false);
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'critical':
        return <AlertCircle className="w-5 h-5 text-red-600" />;
      case 'warning':
        return <AlertTriangle className="w-5 h-5 text-yellow-600" />;
      case 'info':
        return <Info className="w-5 h-5 text-blue-600" />;
      default:
        return <Info className="w-5 h-5 text-gray-600" />;
    }
  };

  const getSeverityBg = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'bg-red-50 border-red-200';
      case 'warning':
        return 'bg-yellow-50 border-yellow-200';
      case 'info':
        return 'bg-blue-50 border-blue-200';
      default:
        return 'bg-gray-50 border-gray-200';
    }
  };

  return (
    <div className="w-full max-w-6xl mx-auto space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">{trackedScenario.play.title}</h2>
            <p className="text-gray-600 mb-4">{trackedScenario.scenario.description}</p>
            <div className="flex items-center gap-4 text-sm">
              <div className="flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-primary-600" />
                <span className="font-semibold">
                  {Math.round(trackedScenario.play.confidence_score * 100)}% Confidence
                </span>
              </div>
              <div className="text-gray-500">
                Last Updated: {new Date(trackedScenario.last_updated).toLocaleString()}
              </div>
            </div>
          </div>
          <div className="flex gap-2">
            <button
              onClick={handleRefresh}
              disabled={refreshing}
              className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:bg-gray-400 transition-colors"
            >
              <RefreshCw className={`w-4 h-4 ${refreshing ? 'animate-spin' : ''}`} />
              Refresh
            </button>
            <button
              onClick={onStop}
              className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
            >
              Stop Tracking
            </button>
          </div>
        </div>
      </div>

      {/* Alerts */}
      {trackedScenario.alerts.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-bold text-gray-900 mb-4">Alerts</h3>
          <div className="space-y-3">
            {trackedScenario.alerts.slice(0, 5).map((alert) => (
              <div
                key={alert.id}
                className={`flex items-start gap-3 p-4 rounded-lg border ${getSeverityBg(alert.severity)}`}
              >
                {getSeverityIcon(alert.severity)}
                <div className="flex-1">
                  <p className="text-gray-900">{alert.message}</p>
                  <p className="text-xs text-gray-500 mt-1">
                    {new Date(alert.created_at).toLocaleString()}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Play Updates */}
      {trackedScenario.play_updates.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-bold text-gray-900 mb-4">Play Updates</h3>
          <div className="space-y-3">
            {trackedScenario.play_updates.map((update, index) => (
              <div key={index} className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                <p className="text-gray-900">{update}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* News Articles */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-bold text-gray-900 mb-4">Recent News</h3>
        <div className="space-y-4">
          {trackedScenario.news_articles.length > 0 ? (
            trackedScenario.news_articles.map((article, index) => (
              <div key={index} className="border-b border-gray-200 pb-4 last:border-0">
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <a
                      href={article.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-lg font-semibold text-primary-600 hover:text-primary-700 flex items-center gap-2"
                    >
                      {article.title}
                      <ExternalLink className="w-4 h-4" />
                    </a>
                    <p className="text-sm text-gray-600 mt-1">{article.summary}</p>
                    <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
                      <span>{article.source}</span>
                      <span>•</span>
                      <span>{new Date(article.published_at).toLocaleDateString()}</span>
                      <span>•</span>
                      <span>Relevance: {Math.round(article.relevance_score * 100)}%</span>
                    </div>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <p className="text-gray-500">No news articles available yet.</p>
          )}
        </div>
      </div>
    </div>
  );
}
