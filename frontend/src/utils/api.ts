import axios from 'axios';
import type { Conversation, EmotionAnalysis } from '../types';

const BASE_URL = 'http://localhost:5000';

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

export const apiClient = {
  async getConversations() {
    return api.get<Conversation[]>('/api/conversations');
  },
  
  async getConversation(id: string) {
    return api.get<Conversation>(`/api/conversations/${id}`);
  },
  
  async analyzeText(text: string) {
    return api.post<EmotionAnalysis[]>('/api/analyze', { text });
  },
  
  async getEmotionAnalytics() {
    return api.get('/api/analytics/emotions');
  },
  
  async getComplianceAnalytics() {
    return api.get('/api/analytics/compliance');
  }
};