import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper,
  Button, CircularProgress, Typography, Modal, Box, TableSortLabel
} from '@mui/material';

function App() {
  const [customers, setCustomers] = useState([]);
  const [sortedCustomers, setSortedCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCustomer, setSelectedCustomer] = useState(null);
  const [order, setOrder] = useState('asc');
  const [orderBy, setOrderBy] = useState('totalSpent');

  // Fetch data from Flask API using Axios
  useEffect(() => {
    axios.get('http://127.0.0.1:5000/high-value-customers')
      .then(response => {
        setCustomers(response.data);
        setSortedCustomers(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        setLoading(false);
      });
  }, []);

  // Sorting function
  const handleRequestSort = (property) => {
    const isAsc = orderBy === property && order === 'asc';
    setOrder(isAsc ? 'desc' : 'asc');
    setOrderBy(property);
    sortData(property, isAsc ? 'desc' : 'asc');
  };

  // Sort data based on a property and order (asc or desc)
  const sortData = (property, order) => {
    const sortedData = [...customers].sort((a, b) => {
      if (order === 'asc') {
        return a[property] < b[property] ? -1 : 1;
      } else {
        return a[property] < b[property] ? 1 : -1;
      }
    });
    setSortedCustomers(sortedData);
  };

  // Handle customer details view
  const handleViewDetails = (customerId) => {
    const customer = customers.find(c => c.customerId === customerId);
    setSelectedCustomer(customer);
  };

  // Modal to display customer details
  const CustomerDetailsModal = () => (
    <Modal open={Boolean(selectedCustomer)} onClose={() => setSelectedCustomer(null)}>
      <Box sx={{
        position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)',
        backgroundColor: 'white', padding: 2, borderRadius: 1, boxShadow: 3
      }}>
        {selectedCustomer && (
          <>
            <Typography variant="h5">Customer Details</Typography>
            <Typography><strong>Name:</strong> {selectedCustomer.name}</Typography>
            <Typography><strong>Email:</strong> {selectedCustomer.email}</Typography>
            <Typography><strong>Total Spent:</strong> ${selectedCustomer.totalSpent}</Typography>
            <Typography><strong>Average Order Value:</strong> ${selectedCustomer.averageOrderValue}</Typography>
            <Typography><strong>Loyalty Tier:</strong> {selectedCustomer.loyaltyTier}</Typography>
            <Typography><strong>Favorite Category:</strong> {selectedCustomer.favoriteCategory}</Typography>
            <Typography><strong>Category Wise Spend:</strong></Typography>
            {selectedCustomer.categoryWiseSpend.map((category, index) => (
              <div key={index}>{category.category}: ${category.spend}</div>
            ))}
            <Button onClick={() => setSelectedCustomer(null)} variant="contained">Close</Button>
          </>
        )}
      </Box>
    </Modal>
  );

  // If loading, display a loader
  if (loading) {
    return <CircularProgress />;
  }

  // If no data is returned
  if (sortedCustomers.length === 0) {
    return <Typography variant="h6">No high-value customers found.</Typography>;
  }

  return (
    <div>
      <Typography variant="h4" gutterBottom>High Value Customers</Typography>

      {/* Table with sorted customers */}
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} aria-label="high value customers table">
          <TableHead>
            <TableRow>
              <TableCell>
                <TableSortLabel
                  active={orderBy === 'customerId'}
                  direction={orderBy === 'customerId' ? order : 'asc'}
                  onClick={() => handleRequestSort('customerId')}
                >
                  Customer ID
                </TableSortLabel>
              </TableCell>
              <TableCell>
                <TableSortLabel
                  active={orderBy === 'name'}
                  direction={orderBy === 'name' ? order : 'asc'}
                  onClick={() => handleRequestSort('name')}
                >
                  Name
                </TableSortLabel>
              </TableCell>
              <TableCell>
                <TableSortLabel
                  active={orderBy === 'email'}
                  direction={orderBy === 'email' ? order : 'asc'}
                  onClick={() => handleRequestSort('email')}
                >
                  Email
                </TableSortLabel>
              </TableCell>
              <TableCell>
                <TableSortLabel
                  active={orderBy === 'totalSpent'}
                  direction={orderBy === 'totalSpent' ? order : 'asc'}
                  onClick={() => handleRequestSort('totalSpent')}
                >
                  Total Spent
                </TableSortLabel>
              </TableCell>
              <TableCell>
                <TableSortLabel
                  active={orderBy === 'averageOrderValue'}
                  direction={orderBy === 'averageOrderValue' ? order : 'asc'}
                  onClick={() => handleRequestSort('averageOrderValue')}
                >
                  Average Order Value
                </TableSortLabel>
              </TableCell>
              <TableCell>
                <TableSortLabel
                  active={orderBy === 'loyaltyTier'}
                  direction={orderBy === 'loyaltyTier' ? order : 'asc'}
                  onClick={() => handleRequestSort('loyaltyTier')}
                >
                  Loyalty Tier
                </TableSortLabel>
              </TableCell>
              <TableCell>Action</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {sortedCustomers.map((customer) => (
              <TableRow key={customer.customerId}>
                <TableCell>{customer.customerId}</TableCell>
                <TableCell>{customer.name}</TableCell>
                <TableCell>{customer.email}</TableCell>
                <TableCell>{customer.totalSpent}</TableCell>
                <TableCell>{customer.averageOrderValue}</TableCell>
                <TableCell>{customer.loyaltyTier}</TableCell>
                <TableCell>
                  <Button onClick={() => handleViewDetails(customer.customerId)} variant="outlined">View Details</Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Customer Details Modal */}
      <CustomerDetailsModal />
    </div>
  );
}

export default App;
