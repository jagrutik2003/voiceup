import { Chip } from '@mui/material';

interface EmotionBadgeProps {
  label: string;
  score: number;
}

export default function EmotionBadge({ label, score }: EmotionBadgeProps) {
  return (
    <Chip
      label={`${label}: ${(score * 100).toFixed(1)}%`}
      color={label === 'happy' ? 'success' : label === 'angry' ? 'error' : 'default'}
      size="small"
      sx={{ mr: 1 }}
    />
  );
}