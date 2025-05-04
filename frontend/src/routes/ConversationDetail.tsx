import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Box, Grid, Typography, Button, Alert } from '@mui/material';
import MessageList from '@components/MessageList';
import CompliancePanel from '@components/CompliancePanel';
import { fetchConversation, analyzeConversation } from '@utils/api';
import { ConversationDetail } from '@types';

export default function ConversationDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [conversation, setConversation] = useState<ConversationDetail | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) {
      const fetchData = async () => {
        setLoading(true);
        try {
          const data = await fetchConversation(id);
          setConversation(data);
          setError(null);
        } catch (err) {
          console.error('Error fetching conversation:', err);
          setError('Failed to load conversation. Please try again later.');
        } finally {
          setLoading(false);
        }
      };
      fetchData();
    }
  }, [id]);

  const handleAnalyze = async () => {
    if (id) {
      try {
        const analysis = await analyzeConversation(id);
        setConversation((prev: ConversationDetail | null) => 
          prev ? { ...prev, analysis } : null
        );
      } catch (error) {
        console.error('Error analyzing conversation:', error);
        setError('Failed to analyze conversation.');
      }
    }
  };

  if (loading) {
    return <Typography>Loading...</Typography>;
  }

  if (error) {
    return (
      <Box>
        <Typography variant="h4" gutterBottom>Conversation</Typography>
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  }

  if (!conversation) {
    return <Typography>Conversation not found.</Typography>;
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>Conversation {id}</Typography>
      <Grid container spacing={2}>
        <Grid item xs={12} md={8}>
          <MessageList messages={conversation.messages} />
        </Grid>
        <Grid item xs={12} md={4}>
          <Button variant="contained" onClick={handleAnalyze} sx={{ mb: 2 }}>
            Analyze Conversation
          </Button>
          <CompliancePanel analysis={conversation.analysis} />
        </Grid>
      </Grid>
    </Box>
  );
}