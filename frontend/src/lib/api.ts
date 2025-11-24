import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface Scenario {
  id: string;
  description: string;
  interpreted_scenario: string;
  plays: Play[];
  created_at: string;
  is_tracking: boolean;
}

export interface Play {
  id: string;
  asset_class: 'equity' | 'commodity' | 'fixed_income';
  title: string;
  description: string;
  action: string;
  instruments: string[];
  rationale: string;
  risk_level: string;
  time_horizon: string;
  confidence_score: number;
}

export interface NewsArticle {
  title: string;
  url: string;
  source: string;
  published_at: string;
  summary: string;
  relevance_score: number;
}

export interface Alert {
  id: string;
  scenario_id: string;
  play_id: string;
  message: string;
  severity: 'info' | 'warning' | 'critical';
  created_at: string;
}

export interface TrackedScenario {
  scenario: Scenario;
  play: Play;
  news_articles: NewsArticle[];
  alerts: Alert[];
  last_updated: string;
  play_updates: string[];
}

export const scenarioAPI = {
  create: async (description: string): Promise<Scenario> => {
    const response = await api.post('/scenarios', { description });
    return response.data;
  },

  list: async (): Promise<Scenario[]> => {
    const response = await api.get('/scenarios');
    return response.data;
  },

  get: async (id: string): Promise<Scenario> => {
    const response = await api.get(`/scenarios/${id}`);
    return response.data;
  },
};

export const trackingAPI = {
  start: async (scenario_id: string, play_id: string): Promise<TrackedScenario> => {
    const response = await api.post('/tracking/start', { scenario_id, play_id });
    return response.data;
  },

  list: async (): Promise<TrackedScenario[]> => {
    const response = await api.get('/tracking');
    return response.data;
  },

  get: async (scenario_id: string, play_id: string): Promise<TrackedScenario> => {
    const response = await api.get(`/tracking/${scenario_id}/${play_id}`);
    return response.data;
  },

  refresh: async (scenario_id: string, play_id: string): Promise<TrackedScenario> => {
    const response = await api.post(`/tracking/${scenario_id}/${play_id}/refresh`);
    return response.data;
  },

  stop: async (scenario_id: string, play_id: string): Promise<void> => {
    await api.delete(`/tracking/${scenario_id}/${play_id}`);
  },
};

export default api;
