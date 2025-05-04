import { useEffect, useState } from 'react';
import { List, ListItem, ListItemText, Typography } from '@mui/material';
import { analyzeMessage } from '@utils/api';

interface Message {
  id: number;
  sender: string;
  text: string;
  timestamp: string;
}

interface Emotion {
  label: string;
  score: number;
}

interface MessageListProps {
  messages: Message[];
}

export default function MessageList({ messages }: MessageListProps) {
  const [emotions, setEmotions] = useState<Record<number, Emotion[]>>({});

  useEffect(() => {
    const fetchEmotions = async () => {
      for (const msg of messages) {
        try {
          const result = await analyzeMessage(msg.id);
          setEmotions((prev) => ({ ...prev, [msg.id]: result.emotions }));
        } catch (error) {
          console.error(`Error analyzing message ${msg.id}:`, error);
        }
      }
    };
    fetchEmotions();
  }, [messages]);

  return (
    <List>
      {messages.map((msg) => (
        <ListItem key={msg.id}>
          <ListItemText
            primary={`${msg.sender}: ${msg.text}`}
            secondary={
              <>
                <Typography variant="caption">{new Date(msg.timestamp).toLocaleString()}</Typography>
                {emotions[msg.id] && (
                  <Typography variant="caption" color="textSecondary">
                    {' | Emotions: ' + emotions[msg.id]
                      .map((e) => `${e.label} (${(e.score * 100).toFixed(1)}%)`)
                      .join(', ')}
                  </Typography>
                )}
              </>
            }
          />
        </ListItem>
      ))}
    </List>
  );
}