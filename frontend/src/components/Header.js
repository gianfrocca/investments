import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

function Header({ user, onLogout }) {
  return (
    <header className="header">
      <div className="header-container">
        <div className="logo">
          <Link to="/dashboard">📈 Investment Tracker</Link>
        </div>

        <nav className="nav">
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/portfolios">Portfolios</Link>
          <Link to="/import">Import</Link>
          <Link to="/backup">Backup</Link>
        </nav>

        <div className="user-menu">
          {user && <span className="user-name">{user.username}</span>}
          <button onClick={onLogout} className="btn btn-secondary">
            Logout
          </button>
        </div>
      </div>
    </header>
  );
}

export default Header;
