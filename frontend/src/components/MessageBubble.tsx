import { Box, Typography } from '@mui/material';
import { Message } from '@types';

interface MessageBubbleProps {
  message: Message;
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isAgent = message.sender === 'agent';

  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: isAgent ? 'flex-end' : 'flex-start',
        mb: 1
      }}
    >
      <Box
        sx={{
          maxWidth: '70%',
          p: 1,
          borderRadius: 2,
          bgcolor: isAgent ? '#1976d2' : '#e0e0e0',
          color: isAgent ? 'white' : 'black'
        }}
      >
        <Typography variant="body2">{message.text}</Typography>
        <Typography variant="caption">{new Date(message.timestamp).toLocaleString()}</Typography>
      </Box>
    </Box>
  );
}