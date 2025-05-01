export interface Message {
  id: number;
  sender: 'agent' | 'customer';
  text: string;
  timestamp: string;
  emotion: string;
}

export interface Conversation {
  id: number;
  created_at: string;
  messages: Message[];
  analysis: {
    emotion_summary: {
      [key: string]: number;
    };
    compliance_summary: {
      rules: ComplianceRule[];
      overall_score: number;
    };
  };
}

export interface EmotionAnalysis {
  text: string;
  emotion: string;
  confidence: number;
}

export interface ComplianceRule {
  id: number;
  name: string;
  description: string;
  passed: boolean;
}

export interface ComplianceData {
  compliance_rate: number;
  total_conversations: number;
  compliant_conversations: number;
  rule_violations: { [key: string]: number };
}

export interface AnalyticsData {
  emotions: {
    distribution: { [key: string]: number };
    trend: Array<{ date: string; emotions: { [key: string]: number } }>;
  };
  compliance: {
    overall_rate: number;
    total_conversations: number;
    compliant_conversations: number;
    rule_violations: { [key: string]: number };
  };
}