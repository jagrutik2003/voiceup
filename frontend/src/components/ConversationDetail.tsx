import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Box, Paper, Typography, CircularProgress, Stack, Chip } from '@mui/material';
import { apiClient } from '../utils/api';
import type { Conversation } from '../types';

const ConversationDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [conversation, setConversation] = useState<Conversation | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchConversation = async () => {
      try {
        const response = await apiClient.getConversation(id!);
        setConversation(response.data);
      } catch (error) {
        console.error('Error fetching conversation:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchConversation();
  }, [id]);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (!conversation) {
    return <Typography color="error">Conversation not found</Typography>;
  }

  return (
    <Stack spacing={3}>
      <Paper sx={{ p: 2 }}>
        <Typography variant="h4" gutterBottom>
          Conversation #{id}
        </Typography>
        <Typography color="text.secondary">
          Created: {new Date(conversation.created_at).toLocaleString()}
        </Typography>
      </Paper>

      <Stack direction={{ xs: 'column', md: 'row' }} spacing={2}>
        <Paper sx={{ p: 2, flex: 1 }}>
          <Typography variant="h6" gutterBottom>
            Messages
          </Typography>
          <Stack spacing={1}>
            {conversation.messages.map((message) => (
              <Box
                key={message.id}
                sx={{
                  alignSelf: message.sender === 'agent' ? 'flex-start' : 'flex-end',
                  maxWidth: '80%'
                }}
              >
                <Paper
                  sx={{
                    p: 2,
                    bgcolor: message.sender === 'agent' ? 'primary.main' : 'secondary.main',
                    color: 'white'
                  }}
                >
                  <Typography variant="caption" display="block">
                    {message.sender.toUpperCase()}
                  </Typography>
                  <Typography>{message.text}</Typography>
                </Paper>
              </Box>
            ))}
          </Stack>
        </Paper>

        {conversation.analysis && (
          <Paper sx={{ p: 2, flex: { xs: 1, md: 0.4 } }}>
            <Typography variant="h6" gutterBottom>
              Analysis
            </Typography>
            <Typography variant="h3" color="primary" align="center">
              {conversation.analysis.overall_compliance_score}%
            </Typography>
            <Typography variant="subtitle1" align="center" gutterBottom>
              Compliance Score
            </Typography>
          </Paper>
        )}
      </Stack>
    </Stack>
  );
};

export default ConversationDetail;