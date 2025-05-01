import React, { useState, useEffect } from 'react';
import { Box, Paper, Typography, CircularProgress, Stack, Alert } from '@mui/material';
import { Bar, Pie } from 'react-chartjs-2';
import { apiClient } from '../utils/api';
import type { AnalyticsData } from '../types';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

const Dashboard: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const [emotionsRes, complianceRes] = await Promise.all([
          apiClient.getEmotionAnalytics(),
          apiClient.getComplianceAnalytics()
        ]);
        
        setAnalytics({
          emotions: emotionsRes.data,
          compliance: complianceRes.data
        });
      } catch (err) {
        setError('Failed to load analytics data');
        console.error('Analytics error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchAnalytics();
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" p={4}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box p={3}>
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  }

  if (!analytics) {
    return (
      <Box p={3}>
        <Alert severity="info">No analytics data available</Alert>
      </Box>
    );
  }

  const emotionDistributionData = {
    labels: Object.keys(analytics?.emotions?.distribution ?? {}),
    datasets: [{
      label: 'Emotions',
      data: Object.values(analytics?.emotions?.distribution ?? {}),
      backgroundColor: [
        'rgba(255, 99, 132, 0.5)',
        'rgba(54, 162, 235, 0.5)',
        'rgba(255, 206, 86, 0.5)',
        'rgba(75, 192, 192, 0.5)',
      ]
    }]
  };

  const complianceData = {
    labels: ['Compliant', 'Non-Compliant'],
    datasets: [{
      data: [
        analytics?.compliance?.compliant_conversations ?? 0,
        (analytics?.compliance?.total_conversations ?? 0) - 
        (analytics?.compliance?.compliant_conversations ?? 0)
      ],
      backgroundColor: [
        'rgba(75, 192, 192, 0.5)',
        'rgba(255, 99, 132, 0.5)'
      ]
    }]
  };

  const violationsData = {
    labels: Object.keys(analytics?.compliance?.rule_violations ?? {}),
    datasets: [{
      label: 'Violations',
      data: Object.values(analytics?.compliance?.rule_violations ?? {}),
      backgroundColor: 'rgba(255, 159, 64, 0.5)'
    }]
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        VoiceUp Analytics Dashboard
      </Typography>
      
      <Stack spacing={3}>
        {/* Emotion Distribution */}
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Customer Emotion Distribution
          </Typography>
          <Box sx={{ height: 300 }}>
            <Bar
              data={emotionDistributionData}
              options={{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                  legend: {
                    position: 'top' as const
                  }
                }
              }}
            />
          </Box>
        </Paper>

        <Stack direction={{ xs: 'column', md: 'row' }} spacing={2}>
          {/* Compliance Rate */}
          <Paper sx={{ p: 2, flex: 1 }}>
            <Typography variant="h6" gutterBottom>
              Compliance Overview
            </Typography>
            <Box sx={{ height: 300 }}>
              <Pie
                data={complianceData}
                options={{
                  responsive: true,
                  maintainAspectRatio: false
                }}
              />
            </Box>
            <Typography variant="h4" color="primary" align="center" sx={{ mt: 2 }}>
              {analytics?.compliance?.compliance_rate ?? 0}%
            </Typography>
            <Typography variant="subtitle1" align="center">
              Overall Compliance Rate
            </Typography>
          </Paper>

          {/* Rule Violations */}
          <Paper sx={{ p: 2, flex: 1 }}>
            <Typography variant="h6" gutterBottom>
              Rule Violations
            </Typography>
            <Box sx={{ height: 300 }}>
              <Bar
                data={violationsData}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  indexAxis: 'y' as const
                }}
              />
            </Box>
          </Paper>
        </Stack>
      </Stack>
    </Box>
  );
};

export default Dashboard;