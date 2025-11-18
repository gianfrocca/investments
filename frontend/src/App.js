import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';

import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Portfolios from './pages/Portfolios';
import PortfolioDetail from './pages/PortfolioDetail';
import AssetDetail from './pages/AssetDetail';
import Import from './pages/Import';
import Backup from './pages/Backup';
import Header from './components/Header';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('token');
    if (token) {
      setIsAuthenticated(true);
      // Optionally fetch user data
    }
  }, []);

  const handleLogin = (token, userData) => {
    localStorage.setItem('token', token);
    setIsAuthenticated(true);
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
    setUser(null);
  };

  return (
    <Router>
      <div className="App">
        {isAuthenticated && <Header user={user} onLogout={handleLogout} />}

        <Routes>
          <Route
            path="/login"
            element={
              isAuthenticated ?
              <Navigate to="/dashboard" /> :
              <Login onLogin={handleLogin} />
            }
          />
          <Route
            path="/register"
            element={
              isAuthenticated ?
              <Navigate to="/dashboard" /> :
              <Register onRegister={handleLogin} />
            }
          />

          {/* Protected routes */}
          <Route
            path="/dashboard"
            element={
              isAuthenticated ?
              <Dashboard /> :
              <Navigate to="/login" />
            }
          />
          <Route
            path="/portfolios"
            element={
              isAuthenticated ?
              <Portfolios /> :
              <Navigate to="/login" />
            }
          />
          <Route
            path="/portfolio/:id"
            element={
              isAuthenticated ?
              <PortfolioDetail /> :
              <Navigate to="/login" />
            }
          />
          <Route
            path="/asset/:id"
            element={
              isAuthenticated ?
              <AssetDetail /> :
              <Navigate to="/login" />
            }
          />
          <Route
            path="/import"
            element={
              isAuthenticated ?
              <Import /> :
              <Navigate to="/login" />
            }
          />
          <Route
            path="/backup"
            element={
              isAuthenticated ?
              <Backup /> :
              <Navigate to="/login" />
            }
          />

          <Route path="/" element={<Navigate to="/dashboard" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
