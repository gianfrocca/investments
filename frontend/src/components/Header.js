import React from 'react';
import { Link } from 'react-router-dom';
import { useLanguage } from '../contexts/LanguageContext';
import './Header.css';

function Header({ user, onLogout }) {
  const { t, language, setLanguage } = useLanguage();

  const toggleLanguage = () => {
    setLanguage(language === 'en' ? 'it' : 'en');
  };

  return (
    <header className="header">
      <div className="header-container">
        <div className="logo">
          <Link to="/dashboard">📈 Investment Tracker</Link>
        </div>

        <nav className="nav">
          <Link to="/dashboard">{t('dashboard')}</Link>
          <Link to="/portfolios">{t('portfolios')}</Link>
          <Link to="/import">{t('import')}</Link>
          <Link to="/backup">{t('backup')}</Link>
        </nav>

        <div className="user-menu">
          <button onClick={toggleLanguage} className="btn btn-secondary" style={{ marginRight: '10px' }}>
            {language === 'en' ? 'IT 🇮🇹' : 'EN 🇬🇧'}
          </button>

          {user && <span className="user-name">{user.username}</span>}
          <button onClick={onLogout} className="btn btn-secondary">
            {t('logout')}
          </button>
        </div>
      </div>
    </header>
  );
}

export default Header;
