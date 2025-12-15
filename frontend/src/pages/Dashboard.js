import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { portfolioAPI } from '../api';
import './Dashboard.css';
import { useLanguage } from '../contexts/LanguageContext';

function Dashboard() {
  const [portfolios, setPortfolios] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { t } = useLanguage();

  useEffect(() => {
    fetchPortfolios();
  }, []);

  const fetchPortfolios = async () => {
    try {
      const response = await portfolioAPI.list();
      setPortfolios(response.data);
    } catch (err) {
      setError(t('failedToLoad'));
    } finally {
      setLoading(false);
    }
  };

  const calculateTotals = () => {
    return portfolios.reduce(
      (acc, portfolio) => {
        if (portfolio.stats) {
          acc.totalValue += portfolio.stats.total_value || 0;
          acc.totalInvested += portfolio.stats.total_invested || 0;
          acc.totalGainLoss += portfolio.stats.total_gain_loss || 0;
        }
        return acc;
      },
      { totalValue: 0, totalInvested: 0, totalGainLoss: 0 }
    );
  };

  if (loading) return (
    <div className="main-content">
      <div className="container" style={{ textAlign: 'center', marginTop: '50px' }}>
        <div className="loading-spinner"></div>
        <p>{t('loading')}</p>
      </div>
    </div>
  );
  if (error) return <div className="error">{error}</div>;

  const totals = calculateTotals();
  const totalGainLossPercentage =
    totals.totalInvested > 0
      ? ((totals.totalGainLoss / totals.totalInvested) * 100).toFixed(2)
      : 0;

  return (
    <div className="main-content">
      <div className="container">
        <h1>{t('dashboard')}</h1>

        <div className="stats-grid">
          <div className="stat-card">
            <h3>{t('totalPortfolioValue')}</h3>
            <p className="stat-value">€{totals.totalValue.toFixed(2)}</p>
          </div>

          <div className="stat-card">
            <h3>{t('totalInvested')}</h3>
            <p className="stat-value">€{totals.totalInvested.toFixed(2)}</p>
          </div>

          <div className="stat-card">
            <h3>{t('totalGainLoss')}</h3>
            <p className={`stat-value ${totals.totalGainLoss >= 0 ? 'positive' : 'negative'}`}>
              €{totals.totalGainLoss.toFixed(2)} ({totalGainLossPercentage}%)
            </p>
          </div>

          <div className="stat-card">
            <h3>{t('portfolios')}</h3>
            <p className="stat-value">{portfolios.length}</p>
          </div>
        </div>

        <div className="card" style={{ marginTop: '30px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
            <h2>{t('yourPortfolios')}</h2>
            <Link to="/portfolios" className="btn btn-primary">
              {t('managePortfolios')}
            </Link>
          </div>

          {portfolios.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
              <p>{t('noPortfolios')}</p>
              <Link to="/portfolios" className="btn btn-primary" style={{ marginTop: '30px', display: 'inline-block' }}>
                {t('createPortfolio')}
              </Link>
            </div>
          ) : (
            <div className="portfolio-list">
              {portfolios.map((portfolio) => (
                <Link
                  key={portfolio.id}
                  to={`/portfolio/${portfolio.id}`}
                  className="portfolio-item"
                >
                  <div>
                    <h3>{portfolio.name}</h3>
                    {portfolio.description && <p>{portfolio.description}</p>}
                    {portfolio.stats && (
                      <div className="portfolio-stats">
                        <span>{t('assets')}: {portfolio.stats.asset_count}</span>
                        <span>{t('value')}: €{portfolio.stats.total_value.toFixed(2)}</span>
                        <span className={portfolio.stats.total_gain_loss >= 0 ? 'positive' : 'negative'}>
                          {portfolio.stats.total_gain_loss >= 0 ? '+' : ''}
                          {portfolio.stats.total_gain_loss_percentage.toFixed(2)}%
                        </span>
                      </div>
                    )}
                  </div>
                  <div className="arrow">→</div>
                </Link>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
