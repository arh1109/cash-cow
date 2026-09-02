import { Container, Typography, Box} from '@mui/material'
import AppHeader from './components/layout/AppHeader.jsx'
import LoginForm from './components/auth/LoginForm.jsx';
import RobotDataGrid from './components/robots/ATMDataGrid.jsx';
import { AuthProvider, useAuth } from './context/AuthContext.jsx';

function Dashboard(){
  const {user, logout} = useAuth()
  return (
    <>
      <AppHeader username={user?.sub} role={user?.role} onLogout={logout} />
      <Container maxWidth="lg" sx={{ mt: 4}}>
        <Typography variant="h5" component="h2" gutterBottom>
          Fleet Overview
        </Typography>
        <Box sx={{ mb: 4}}>
          < ATMDataGrid />
        </Box>
      </Container>
    </>
  )
}

//conditional layout switcher component that renders either the Dashboard or the login form
//based on the user's authentication status, tracked in the global AuthContext
function AppContent() {
  const {isAuthenticated } = useAuth();
  return isAuthenticated ? <Dashboard /> : <LoginForm />;
}

//acts as a root application component that wraps the entire app in the AuthProvider context
function App(){
  return (
      <AuthProvider>
        <AppContent />
      </AuthProvider>
  )
}

export default App;
