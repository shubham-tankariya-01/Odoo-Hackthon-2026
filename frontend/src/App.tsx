import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from './components/layout/Layout';

// Pages
import { Login } from './pages/Login';
import { Dashboard } from './pages/Dashboard';
import { Organization } from './pages/Organization';
import { Assets } from './pages/Assets';
import { Transfers } from './pages/Transfers';
import { Booking } from './pages/Booking';
import { Maintenance } from './pages/Maintenance';
import { Audit } from './pages/Audit';
import { Reports } from './pages/Reports';
import { Activity } from './pages/Activity';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        
        <Route element={<Layout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/organization" element={<Organization />} />
          <Route path="/assets" element={<Assets />} />
          <Route path="/transfers" element={<Transfers />} />
          <Route path="/booking" element={<Booking />} />
          <Route path="/maintenance" element={<Maintenance />} />
          <Route path="/audit" element={<Audit />} />
          <Route path="/reports" element={<Reports />} />
          <Route path="/notifications" element={<Activity />} />
        </Route>
        
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
