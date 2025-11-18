import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { portfolioAPI } from '../api';

function Portfolios() {
  const [portfolios, setPortfolios] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({ name: '', description: '' });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    fetchPortfolios();
  }, []);

  const fetchPortfolios = async () => {
    try {
      const response = await portfolioAPI.list();
      setPortfolios(response.data);
    } catch (err) {
      setError('Failed to load portfolios');
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
      setSuccess('Portfolio created successfully!');
      setFormData({ name: '', description: '' });
      setShowForm(false);
      fetchPortfolios();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create portfolio');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this portfolio?')) {
      return;
    }

    try {
      await portfolioAPI.delete(id);
      setSuccess('Portfolio deleted successfully');
      fetchPortfolios();
    } catch (err) {
      setError('Failed to delete portfolio');
    }
  };

  if (loading) return <div className="loading">Loading...</div>;

  return (
    <div className="main-content">
      <div className="container">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h1>Portfolios</h1>
          <button onClick={() => setShowForm(!showForm)} className="btn btn-primary">
            {showForm ? 'Cancel' : '+ New Portfolio'}
          </button>
        </div>

        {error && <div className="error">{error}</div>}
        {success && <div className="success">{success}</div>}

        {showForm && (
          <div className="card">
            <h2>Create New Portfolio</h2>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>Portfolio Name</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  required
                />
              </div>

              <div className="form-group">
                <label>Description (optional)</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  rows="3"
                />
              </div>

              <button type="submit" className="btn btn-primary">
                Create Portfolio
              </button>
            </form>
          </div>
        )}

        <div className="card">
          {portfolios.length === 0 ? (
            <p style={{ textAlign: 'center', color: '#666' }}>No portfolios yet. Create one to get started!</p>
          ) : (
            <table className="table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Description</th>
                  <th>Assets</th>
                  <th>Value</th>
                  <th>Gain/Loss</th>
                  <th>Actions</th>
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
                        Delete
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
