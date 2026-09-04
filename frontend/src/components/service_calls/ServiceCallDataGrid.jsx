import { useEffect, useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import {
    Alert,
    Box,
    Button,
    CircularProgress,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    MenuItem,
    Stack,
    TextField,
} from '@mui/material';

import apiClient from '../../api/client';
import { useAuth } from '../../context/AuthContext.jsx';


const columns = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'title', headerName: 'Title', width: 230 },
    { field: 'priority', headerName: 'Priority', width: 120 },
    { field: 'status', headerName: 'Status', width: 130 },
    { field: 'atm_id', headerName: 'ATM ID', width: 100, type: 'number' },
    {
        field: 'technician_id',
        headerName: 'Technician ID',
        width: 130,
        type: 'number',
    },
];


function ServiceCallDataGrid({ onSuccess }) {
    const { user } = useAuth();

    const [serviceCalls, setServiceCalls] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const [selectedServiceCall, setSelectedServiceCall] = useState(null);
    const [dialogMode, setDialogMode] = useState(null);

    const [searchText, setSearchText] = useState('');
const [searchField, setSearchField] = useState('title');
const [isFiltered, setIsFiltered] = useState(false);

    const [formData, setFormData] = useState({
        title: '',
        priority: 'Medium',
        status: 'Pending',
        atm_id: '',
        technician_id: '',
    });

    const filteredServiceCalls = isFiltered
    ? serviceCalls.filter((serviceCall) => {
        const value = serviceCall[searchField];

        if (value === null || value === undefined) {
            return false;
        }

        return String(value)
            .toLowerCase()
            .includes(searchText.toLowerCase());
    })
    : serviceCalls;

    const isAdmin = user?.role === 'Operations Admin';


    async function fetchServiceCalls() {
        try {
            setLoading(true);

            const response = await apiClient.get('/service_calls');

            setServiceCalls(response.data);
            setError(null);
        } catch (err) {
            console.error(err);
            setError('Could not load service calls');
        } finally {
            setLoading(false);
        }
    }


    useEffect(() => {
        fetchServiceCalls();
    }, []);


    function openAddDialog() {
        setFormData({
            title: '',
            priority: 'Medium',
            status: 'Pending',
            atm_id: '',
            technician_id: '',
        });

        setDialogMode('add');
    }


    function openEditDialog() {
        if (!selectedServiceCall) return;

        setFormData({
            title: selectedServiceCall.title,
            priority: selectedServiceCall.priority,
            status: selectedServiceCall.status,
            atm_id: selectedServiceCall.atm_id,
            technician_id: selectedServiceCall.technician_id,
        });

        setDialogMode('edit');
    }


    function closeDialog() {
        setDialogMode(null);
    }

    function handleSearch() {
    if (!searchText.trim()) return;

    setIsFiltered(true);
    setSelectedServiceCall(null);
}

function handleClearFilter() {
    setSearchText('');
    setIsFiltered(false);
    setSelectedServiceCall(null);
}


    async function handleSave() {
        const payload = {
            title: formData.title,
            priority: formData.priority,
            status: formData.status,
            atm_id: Number(formData.atm_id),
            technician_id: Number(formData.technician_id),
        };

        try {
            if (dialogMode === 'add') {
                await apiClient.post('/service_calls', payload);

                onSuccess?.('Service call created successfully');
            }

            if (dialogMode === 'edit') {
                await apiClient.put(
                    `/service_calls/${selectedServiceCall.id}`,
                    payload
                );

                onSuccess?.('Service call updated successfully');
            }

            closeDialog();
            setSelectedServiceCall(null);

            await fetchServiceCalls();
        } catch (err) {
            console.error(err);
            console.error('Backend response:', err.response?.data);

            setError(
                err.response?.data?.detail ||
                'Could not save service call'
            );
        }
    }


    async function handleDelete() {
        if (!selectedServiceCall) return;

        const confirmed = window.confirm(
            `Delete service call "${selectedServiceCall.title}"?`
        );

        if (!confirmed) return;

        try {
            await apiClient.delete(
                `/service_calls/${selectedServiceCall.id}`
            );

            setSelectedServiceCall(null);

            onSuccess?.('Service call deleted successfully');

            await fetchServiceCalls();
        } catch (err) {
            console.error(err);
            console.error('Backend response:', err.response?.data);

            setError(
                err.response?.data?.detail ||
                'Could not delete service call'
            );
        }
    }


    if (loading) {
        return <CircularProgress />;
    }


    return (
        <>
            {error && (
                <Alert severity="error" sx={{ mb: 2 }}>
                    {error}
                </Alert>
            )}

            <Stack
    direction="row"
    spacing={2}
    sx={{ mb: 2 }}
    alignItems="center"
>
    <TextField
        size="small"
        label="Search"
        value={searchText}
        onChange={(e) => setSearchText(e.target.value)}
        onKeyDown={(e) => {
            if (
                e.key === 'Enter' &&
                !isFiltered &&
                searchText.trim()
            ) {
                handleSearch();
            }
        }}
    />

    <TextField
        select
        size="small"
        label="Search Criteria"
        value={searchField}
        onChange={(e) => {
            setSearchField(e.target.value);
            setIsFiltered(false);
        }}
        sx={{ minWidth: 170 }}
    >
        <MenuItem value="id">ID</MenuItem>
        <MenuItem value="title">Title</MenuItem>
        <MenuItem value="priority">Priority</MenuItem>
        <MenuItem value="status">Status</MenuItem>
        <MenuItem value="atm_id">ATM ID</MenuItem>
        <MenuItem value="technician_id">Technician ID</MenuItem>
    </TextField>

    <Button
        variant="outlined"
        onClick={handleSearch}
        disabled={isFiltered || !searchText.trim()}
    >
        Search
    </Button>

    <Button
        variant="outlined"
        onClick={handleClearFilter}
        disabled={!isFiltered}
    >
        Clear Filter
    </Button>

    {isAdmin && (
        <>
            <Button
                variant="contained"
                onClick={openAddDialog}
            >
                Add Service Call
            </Button>

            <Button
                variant="outlined"
                disabled={!selectedServiceCall}
                onClick={openEditDialog}
            >
                Edit Service Call
            </Button>

            <Button
                variant="outlined"
                color="error"
                disabled={!selectedServiceCall}
                onClick={handleDelete}
            >
                Delete Service Call
            </Button>
        </>
    )}
</Stack>

            <Box sx={{ height: 400, width: '100%' }}>
                <DataGrid
                    rows={filteredServiceCalls}
                    columns={columns}
                    getRowId={(row) => row.id}
                    onRowClick={(params) => {
                        setSelectedServiceCall(params.row);
                    }}
                />
            </Box>

            <Dialog
                open={dialogMode !== null}
                onClose={closeDialog}
                fullWidth
                maxWidth="sm"
            >
                <DialogTitle>
                    {dialogMode === 'add'
                        ? 'Add Service Call'
                        : 'Edit Service Call'}
                </DialogTitle>

                <DialogContent>
                    <Stack spacing={2} sx={{ mt: 1 }}>
                        <TextField
                            label="Title"
                            value={formData.title}
                            onChange={(e) =>
                                setFormData({
                                    ...formData,
                                    title: e.target.value,
                                })
                            }
                        />

                        <TextField
                            select
                            label="Priority"
                            value={formData.priority}
                            onChange={(e) =>
                                setFormData({
                                    ...formData,
                                    priority: e.target.value,
                                })
                            }
                        >
                            <MenuItem value="Low">
                                Low
                            </MenuItem>

                            <MenuItem value="Medium">
                                Medium
                            </MenuItem>

                            <MenuItem value="Critical">
                                Critical
                            </MenuItem>
                        </TextField>

                        <TextField
                            select
                            label="Status"
                            value={formData.status}
                            onChange={(e) =>
                                setFormData({
                                    ...formData,
                                    status: e.target.value,
                                })
                            }
                        >
                            <MenuItem value="Pending">
                                Pending
                            </MenuItem>

                            <MenuItem value="In-Progress">
                                In-Progress
                            </MenuItem>

                            <MenuItem value="Completed">
                                Completed
                            </MenuItem>

                            <MenuItem value="Failed">
                                Failed
                            </MenuItem>
                        </TextField>

                        <TextField
                            label="ATM ID"
                            type="number"
                            value={formData.atm_id}
                            onChange={(e) =>
                                setFormData({
                                    ...formData,
                                    atm_id: e.target.value,
                                })
                            }
                        />

                        <TextField
                            label="Technician ID"
                            type="number"
                            value={formData.technician_id}
                            onChange={(e) =>
                                setFormData({
                                    ...formData,
                                    technician_id: e.target.value,
                                })
                            }
                        />
                    </Stack>
                </DialogContent>

                <DialogActions>
                    <Button onClick={closeDialog}>
                        Cancel
                    </Button>

                    <Button
                        variant="contained"
                        onClick={handleSave}
                    >
                        Save
                    </Button>
                </DialogActions>
            </Dialog>
        </>
    );
}


export default ServiceCallDataGrid;