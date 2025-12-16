import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { portfolioAPI } from '../api';
import { useLanguage } from '../contexts/LanguageContext';

function Portfolios() {
  const [portfolios, setPortfolios] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({ name: '', description: '' });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const { t } = useLanguage();

  useEffect(() => {
    fetchPortfolios();
  }, []);

  const fetchPortfolios = async () => {
    try {
      const response = await portfolioAPI.list();
      if (Array.isArray(response.data)) {
        setPortfolios(response.data);
      } else {
        console.error('Expected array but got:', response.data);
        setPortfolios([]);
        setError(t('failedToLoad') + ': Invalid data format');
      }
    } catch (err) {
      console.error('Error fetching portfolios:', err);
      setError(t('failedToLoad'));
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      await portfolioAPI.create(formData);
      setSuccess(t('successCreated'));
      setFormData({ name: '', description: '' });
      setShowForm(false);
      fetchPortfolios();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create portfolio');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm(t('areYouSureDelete'))) {
      return;
    }

    try {
      await portfolioAPI.delete(id);
      setSuccess(t('successDeleted'));
      fetchPortfolios();
    } catch (err) {
      setError('Failed to delete portfolio');
    }
  };

  if (loading) return (
    <div className="main-content">
      <div className="container" style={{ textAlign: 'center', marginTop: '50px' }}>
        <div className="loading-spinner"></div>
        <p>{t('loading')}</p>
      </div>
    </div>
  );

  return (
    <div className="main-content">
      <div className="container">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h1>{t('portfolios')}</h1>
          <button onClick={() => setShowForm(!showForm)} className="btn btn-primary">
            {showForm ? t('cancel') : t('newPortfolio')}
          </button>
        </div>

        {error && <div className="error">{error}</div>}
        {success && <div className="success">{success}</div>}

        {showForm && (
          <div className="card">
            <h2>{t('createNewPortfolio')}</h2>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>{t('portfolioName')}</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  required
                />
              </div>

              <div className="form-group">
                <label>{t('description')}</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  rows="3"
                />
              </div>

              <button type="submit" className="btn btn-primary">
                {t('createPortfolio')}
              </button>
            </form>
          </div>
        )}

        <div className="card">
          {portfolios.length === 0 ? (
            <p style={{ textAlign: 'center', color: '#666' }}>{t('noPortfolios')}</p>
          ) : (
            <table className="table">
              <thead>
                <tr>
                  <th>{t('name')}</th>
                  <th>{t('description')}</th>
                  <th>{t('assets')}</th>
                  <th>{t('value')}</th>
                  <th>{t('gainLoss')}</th>
                  <th>{t('actions')}</th>
                </tr>
              </thead>
              <tbody>
                {portfolios.map((portfolio) => (
                  <tr key={portfolio.id}>
                    <td>
                      <Link to={`/portfolio/${portfolio.id}`} style={{ color: '#007bff', textDecoration: 'none' }}>
                        {portfolio.name}
                      </Link>
                    </td>
                    <td>{portfolio.description || '-'}</td>
                    <td>{portfolio.stats?.asset_count || 0}</td>
                    <td>€{portfolio.stats?.total_value.toFixed(2) || '0.00'}</td>
                    <td className={portfolio.stats?.total_gain_loss >= 0 ? 'positive' : 'negative'}>
                      {portfolio.stats?.total_gain_loss >= 0 ? '+' : ''}
                      {portfolio.stats?.total_gain_loss_percentage.toFixed(2) || '0.00'}%
                    </td>
                    <td>
                      <button
                        onClick={() => handleDelete(portfolio.id)}
                        className="btn btn-danger"
                        style={{ padding: '5px 10px', fontSize: '14px' }}
                      >
                        {t('delete')}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
}

export default Portfolios;
