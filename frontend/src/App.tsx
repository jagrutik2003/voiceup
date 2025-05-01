import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import Root from './routes/root';
import EmotionAnalyzer from './components/EmotionAnalyzer';
import ConversationList from './components/ConversationList';
import ConversationDetail from './components/ConversationDetail';
import Dashboard from './components/Dashboard';
import { CssBaseline, ThemeProvider } from '@mui/material';
import { theme } from './utils/theme';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Root />,
    children: [
      {
        index: true,
        element: <Dashboard />,
      },
      {
        path: 'analyze',
        element: <EmotionAnalyzer />,
      },
      {
        path: 'conversations',
        element: <ConversationList />,
      },
      {
        path: 'conversations/:id',
        element: <ConversationDetail />,
      }
    ],
  },
]);

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <RouterProvider router={router} />
    </ThemeProvider>
  );
}

export default App;