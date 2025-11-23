'use client';

import { Play } from '@/lib/api';
import { TrendingUp, TrendingDown, BarChart3 } from 'lucide-react';

interface PlayCardProps {
  play: Play;
  scenarioId: string;
  onTrack: (playId: string) => void;
  isTracking?: boolean;
}

export default function PlayCard({ play, scenarioId, onTrack, isTracking }: PlayCardProps) {
  const getAssetIcon = (assetClass: string) => {
    switch (assetClass) {
      case 'equity':
        return <TrendingUp className="w-6 h-6" />;
      case 'commodity':
        return <BarChart3 className="w-6 h-6" />;
      case 'fixed_income':
        return <TrendingDown className="w-6 h-6" />;
      default:
        return <BarChart3 className="w-6 h-6" />;
    }
  };

  const getAssetColor = (assetClass: string) => {
    switch (assetClass) {
      case 'equity':
        return 'bg-blue-100 text-blue-700';
      case 'commodity':
        return 'bg-amber-100 text-amber-700';
      case 'fixed_income':
        return 'bg-green-100 text-green-700';
      default:
        return 'bg-gray-100 text-gray-700';
    }
  };

  const getRiskColor = (riskLevel: string) => {
    switch (riskLevel.toLowerCase()) {
      case 'low':
        return 'text-green-600';
      case 'medium':
        return 'text-yellow-600';
      case 'high':
        return 'text-red-600';
      default:
        return 'text-gray-600';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className={`p-3 rounded-lg ${getAssetColor(play.asset_class)}`}>
            {getAssetIcon(play.asset_class)}
          </div>
          <div>
            <h3 className="text-xl font-bold text-gray-900">{play.title}</h3>
            <p className="text-sm text-gray-500 capitalize">{play.asset_class.replace('_', ' ')}</p>
          </div>
        </div>
        <div className="text-right">
          <div className="text-2xl font-bold text-primary-600">
            {Math.round(play.confidence_score * 100)}%
          </div>
          <div className="text-xs text-gray-500">Confidence</div>
        </div>
      </div>

      <div className="space-y-3 mb-4">
        <div>
          <span className="font-semibold text-gray-700">Action: </span>
          <span className="text-gray-900">{play.action}</span>
        </div>
        
        <div>
          <span className="font-semibold text-gray-700">Instruments: </span>
          <span className="text-gray-900">{play.instruments.join(', ')}</span>
        </div>

        <div>
          <p className="text-gray-600">{play.description}</p>
        </div>

        <div className="bg-gray-50 p-3 rounded">
          <p className="text-sm font-semibold text-gray-700 mb-1">Rationale:</p>
          <p className="text-sm text-gray-600">{play.rationale}</p>
        </div>
      </div>

      <div className="flex items-center justify-between pt-4 border-t border-gray-200">
        <div className="flex gap-4 text-sm">
          <div>
            <span className="text-gray-500">Risk: </span>
            <span className={`font-semibold ${getRiskColor(play.risk_level)}`}>
              {play.risk_level}
            </span>
          </div>
          <div>
            <span className="text-gray-500">Horizon: </span>
            <span className="font-semibold text-gray-900">{play.time_horizon}</span>
          </div>
        </div>

        <button
          onClick={() => onTrack(play.id)}
          disabled={isTracking}
          className="bg-primary-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-primary-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          {isTracking ? 'Tracking...' : 'Track This Play'}
        </button>
      </div>
    </div>
  );
}
