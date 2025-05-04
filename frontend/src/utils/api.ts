import axios from 'axios';
import { Conversation, ConversationDetail, EmotionAnalytics, ComplianceAnalytics, Analysis }from '../types';

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' }
});

export const fetchConversations = async (): Promise<Conversation[]> => {
  const response = await api.get('/conversations');
  return response.data;
};

export const fetchConversation = async (id: string): Promise<ConversationDetail> => {
  const response = await api.get(`/conversations/${id}`);
  return response.data;
};

export const analyzeConversation = async (id: string): Promise<Analysis> => {
  const response = await api.post(`/conversations/${id}/analyze`);
  return response.data;
};

export const fetchEmotionAnalytics = async (): Promise<EmotionAnalytics> => {
  const response = await api.get('/analytics/emotions');
  return response.data;
};

export const fetchComplianceAnalytics = async (): Promise<ComplianceAnalytics> => {
  const response = await api.get('/analytics/compliance');
  return response.data;
};

export const analyzeMessage = async (messageId: number): Promise<{ emotions: { label: string; score: number }[] }> => {
    const response = await api.post(`/messages/${messageId}/analyze`);
    return response.data;
  };

