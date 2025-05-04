import { Outlet } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Container, Box } from '@mui/material';
import { Link } from 'react-router-dom';

export default function Root() {
  return (
    <Box sx={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component={Link} to="/" sx={{ color: 'white', textDecoration: 'none' }}>
            VoiceUp Analytics
          </Typography>
          <Box sx={{ ml: 2 }}>
            <Typography component={Link} to="/conversations" sx={{ color: 'white', textDecoration: 'none', mr: 2 }}>
              Conversations
            </Typography>
          </Box>
        </Toolbar>
      </AppBar>
      <Container sx={{ flex: 1, py: 2 }}>
        <Outlet />
      </Container>
    </Box>
  );
}