import { useEffect, useState } from 'react';
import {
  Alert,
  Box,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  Typography,
} from '@mui/material';

import apiClient from '../../api/client';

export default function LowCashAlert() {
  const [atms, setAtms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLowCashATMs = async () => {
      try {
        const response = await apiClient.get('/atms/low-cash', {
          params: {
            threshold: 20,
          },
        });

        setAtms(response.data);
      } catch (err) {
        console.error(err);
        setError('Unable to load low-cash ATM alerts.');
      } finally {
        setLoading(false);
      }
    };

    fetchLowCashATMs();
  }, []);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', py: 2 }}>
        <CircularProgress size={28} />
      </Box>
    );
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  if (atms.length === 0) {
    return (
      <Alert severity="success">
        No active ATMs are currently below the 20% cash reserve threshold.
      </Alert>
    );
  }

  return (
    <Alert severity="warning">
      <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }}>
        {atms.length} ATM{atms.length !== 1 ? 's' : ''} below 20% cash reserve
      </Typography>

      <List dense>
        {atms.map((atm) => (
          <ListItem key={atm.id}>
            <ListItemText
              primary={`${atm.serial_number} — ${atm.model}`}
              secondary={`Cash Level: ${atm.cash_level}% | Branch: ${atm.branch_id}`}
            />
          </ListItem>
        ))}
      </List>
    </Alert>
  );
}