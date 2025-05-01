import React, { useState } from 'react';
import { Box, TextField, Button, Paper, Typography, Alert, CircularProgress } from '@mui/material';
import { apiClient } from '../utils/api';
import type { EmotionAnalysis } from '../types';

const EmotionAnalyzer: React.FC = () => {
  const [text, setText] = useState('');
  const [result, setResult] = useState<EmotionAnalysis[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const analyzeText = async () => {
    if (!text.trim()) {
      setError('Please enter some text to analyze');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await apiClient.analyzeText(text);
      setResult(response.data);
    } catch (err) {
      setError('Failed to analyze text. Please try again.');
      console.error('Analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto' }}>
      <Typography variant="h4" gutterBottom>
        Emotion Analyzer
      </Typography>
      <TextField
        fullWidth
        multiline
        rows={4}
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Enter text to analyze..."
        sx={{ mb: 2 }}
      />
      <Button
        variant="contained"
        onClick={analyzeText}
        disabled={loading}
        sx={{ mb: 2 }}
      >
        {loading ? <CircularProgress size={24} /> : 'Analyze'}
      </Button>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {result && (
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Analysis Results
          </Typography>
          {result.map((emotion, index) => (
            <Box key={index} sx={{ mb: 1 }}>
              <Typography>
                {emotion.label}: {(emotion.score * 100).toFixed(1)}%
              </Typography>
            </Box>
          ))}
        </Paper>
      )}
    </Box>
  );
};

export default EmotionAnalyzer;