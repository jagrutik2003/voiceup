import { useEffect, useState } from 'react';
import { Box, Grid, Paper, Typography, Alert } from '@mui/material';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import { fetchEmotionAnalytics, fetchComplianceAnalytics } from '@utils/api';
import { EmotionAnalytics, ComplianceAnalytics } from '@types';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default function Dashboard() {
  const [emotionData, setEmotionData] = useState<EmotionAnalytics | null>(null);
  const [complianceData, setComplianceData] = useState<ComplianceAnalytics | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [emotionResponse, complianceResponse] = await Promise.all([
          fetchEmotionAnalytics(),
          fetchComplianceAnalytics()
        ]);
        setEmotionData(emotionResponse);
        setComplianceData(complianceResponse);
      } catch (err) {
        console.error('Error fetching analytics:', err);
        setError('Failed to load analytics data. Please try again later.');
      }
    };
    fetchData();
  }, []);

  const emotionChartData = emotionData
    ? {
        labels: Object.keys(emotionData.distribution),
        datasets: [
          {
            label: 'Emotion Distribution',
            data: Object.values(emotionData.distribution),
            backgroundColor: '#1976d2'
          }
        ]
      }
    : null;

  const complianceChartData = complianceData
    ? {
        labels: Object.keys(complianceData.rule_violations),
        datasets: [
          {
            label: 'Rule Violations',
            data: Object.values(complianceData.rule_violations),
            backgroundColor: '#dc004e'
          }
        ]
      }
    : null;

  const complianceScoreChartData = complianceData
    ? {
        labels: ['0-20', '21-40', '41-60', '61-80', '81-100'],
        datasets: [
          {
            label: 'Compliance Score Distribution',
            data: [
              complianceData.scores.filter(s => s <= 20).length,
              complianceData.scores.filter(s => s > 20 && s <= 40).length,
              complianceData.scores.filter(s => s > 40 && s <= 60).length,
              complianceData.scores.filter(s => s > 60 && s <= 80).length,
              complianceData.scores.filter(s => s > 80).length
            ],
            backgroundColor: '#388e3c'
          }
        ]
      }
    : null;

  return (
    <Box>
      <Typography variant="h4" gutterBottom>Dashboard</Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      <Grid container spacing={2}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6">Emotion Distribution</Typography>
            {emotionChartData ? (
              <Bar data={emotionChartData} options={{ responsive: true }} />
            ) : (
              <Typography>Loading...</Typography>
            )}
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6">Compliance Violations</Typography>
            {complianceChartData ? (
              <Bar data={complianceChartData} options={{ responsive: true }} />
            ) : (
              <Typography>Loading...</Typography>
            )}
          </Paper>
        </Grid>
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6">Compliance Score Distribution</Typography>
            {complianceScoreChartData ? (
              <Bar data={complianceScoreChartData} options={{ responsive: true }} />
            ) : (
              <Typography>Loading...</Typography>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}