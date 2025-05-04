import { Box, Typography, List, ListItem, ListItemText } from '@mui/material';
import { Analysis } from '../types';

interface CompliancePanelProps {
  analysis: Analysis | null;
}

export default function CompliancePanel({ analysis }: CompliancePanelProps) {
  if (!analysis) {
    return <Typography>No analysis available</Typography>;
  }

  return (
    <Box sx={{ border: '1px solid #e0e0e0', p: 2 }}>
      <Typography variant="h6">Compliance Analysis</Typography>
      <Typography>Score: {analysis.overall_compliance_score}%</Typography>
      <List dense>
        {Object.entries(analysis.compliance_summary || {}).map(([rule, passed]) => (
          <ListItem key={rule}>
            <ListItemText
              primary={rule.replace(/_/g, ' ')}
              secondary={passed ? 'Passed' : 'Failed'}
              sx={{ textTransform: 'capitalize' }}
            />
          </ListItem>
        ))}
      </List>
    </Box>
  );
}