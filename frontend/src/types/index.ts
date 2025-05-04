export interface Conversation {
    id: number;
    created_at: string;
    message_count: number;
    analysis?: {
      emotion_summary: { emotions: { label: string; score: number }[] } | null;
      compliance_score: number | null;
    };
  }
  
  export interface Message {
    id: number;
    conversation_id: number;
    sender: string;
    text: string;
    timestamp: string;
  }
  
  export interface Analysis {
    emotion_summary: { emotions: { label: string; score: number }[] } | null;
    compliance_summary: Record<string, boolean> | null;
    overall_compliance_score: number | null;
  }
  
  export interface ConversationDetail {
    id: number;
    created_at: string;
    messages: Message[];
    analysis: Analysis | null;
  }
  
  export interface EmotionAnalytics {
    distribution: Record<string, number>;
    trend: { date: string; emotions: { label: string; score: number }[] }[];
    total_conversations: number;
  }
  
  export interface ComplianceAnalytics {
    compliance_rate: number;
    average_score: number;
    total_conversations: number;
    compliant_conversations: number;
    rule_violations: Record<string, number>;
  }

  export interface ComplianceAnalytics {
    compliance_rate: number;
    average_score: number;
    total_conversations: number;
    compliant_conversations: number;
    rule_violations: Record<string, number>;
    scores: number[];
  }
  
  export interface EmotionAnalytics {
    distribution: Record<string, number>;
    trend: { date: string; emotions: { label: string; score: number }[] }[];
    total_conversations: number;
  }
  