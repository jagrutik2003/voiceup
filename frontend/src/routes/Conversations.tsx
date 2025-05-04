import { useEffect, useState } from 'react';
import { Box, Grid, ListItem, ListItemText, Paper, Typography, Alert } from '@mui/material';
import { Link } from 'react-router-dom';
import { fetchConversations } from '@utils/api';
import { Conversation } from '@types';

export default function Conversations() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const data = await fetchConversations();
        setConversations(data);
        setError(null);
      } catch (err) {
        console.error('Error fetching conversations:', err);
        setError('Failed to load conversations. Please try again later.');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return (
      <Box>
        <Typography variant="h4" gutterBottom>Conversations</Typography>
        <Typography>Loading...</Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Box>
        <Typography variant="h4" gutterBottom>Conversations</Typography>
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>Conversations</Typography>
      {conversations.length === 0 ? (
        <Typography>No conversations available.</Typography>
      ) : (
        <Grid container spacing={2}>
          {conversations.map((conv) => (
            <Grid item xs={12} md={6} key={conv.id}>
              <Paper sx={{ p: 2 }}>
                <ListItem
                  component={Link}
                  to={`/conversations/${conv.id}`}
                  sx={{ textDecoration: 'none' }}
                >
                  <ListItemText
                    primary={new Date(conv.created_at).toLocaleString()}
                    secondary={`Messages: ${conv.message_count}, Compliance: ${conv.analysis?.compliance_score ?? 'N/A'}%`}
                  />
                </ListItem>
              </Paper>
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  );
}