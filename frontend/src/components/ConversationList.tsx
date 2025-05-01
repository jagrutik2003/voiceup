import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  List, 
  ListItem, 
  Typography, 
  Paper, 
  Box, 
  CircularProgress 
} from '@mui/material';
import { apiClient } from '../utils/api';
import type { Conversation } from '../types';

const ConversationList: React.FC = () => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchConversations = async () => {
      try {
        const response = await apiClient.getConversations();
        setConversations(response.data);
      } catch (error) {
        console.error('Error fetching conversations:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchConversations();
  }, []);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Conversations
      </Typography>
      <List>
        {conversations.map((conv) => (
          <ListItem
            key={conv.id}
            component={Link}
            to={`/conversations/${conv.id}`}
            sx={{ textDecoration: 'none', color: 'inherit' }}
          >
            <Paper sx={{ p: 2, width: '100%' }}>
              <Typography variant="h6">
                Conversation #{conv.id}
              </Typography>
              <Typography color="text.secondary">
                Messages: {conv.messages.length}
              </Typography>
              {conv.analysis && (
                <Typography color="text.secondary">
                  Compliance Score: {conv.analysis.overall_compliance_score}%
                </Typography>
              )}
            </Paper>
          </ListItem>
        ))}
      </List>
    </Box>
  );
};

export default ConversationList;