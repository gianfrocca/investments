import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { portfolioAPI, assetAPI, priceAPI } from '../api';

function PortfolioDetail() {
  const { id } = useParams();
  const [portfolio, setPortfolio] = useState(null);
  const [assets, setAssets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [updating, setUpdating] = useState(false);

  useEffect(() => {
    fetchData();
  }, [id]);

  const fetchData = async () => {
    try {
      const [portfolioRes, assetsRes] = await Promise.all([
        portfolioAPI.get(id),
        assetAPI.listByPortfolio(id),
      ]);
      setPortfolio(portfolioRes.data);
      setAssets(assetsRes.data);
    } catch (err) {
      setError('Failed to load portfolio');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdatePrices = async () => {
    setUpdating(true);
    try {
      await priceAPI.updatePortfolio(id);
      alert('Price update started! Refresh the page in a few moments.');
    } catch (err) {
      alert('Failed to update prices');
    } finally {
      setUpdating(false);
    }
  };

  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!portfolio) return <div>Portfolio not found</div>;

  return (
    <div className="main-content">
      <div className="container">
        <div style={{ marginBottom: '20px' }}>
          <Link to="/portfolios">← Back to Portfolios</Link>
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h1>{portfolio.name}</h1>
            {portfolio.description && <p>{portfolio.description}</p>}
          </div>
          <div>
            <button onClick={handleUpdatePrices} className="btn btn-primary" disabled={updating}>
              {updating ? 'Updating...' : '🔄 Update Prices'}
            </button>
          </div>
        </div>

        {portfolio.stats && (
          <div className="stats-grid" style={{ marginTop: '20px' }}>
            <div className="stat-card">
              <h3>Total Value</h3>
              <p className="stat-value">€{portfolio.stats.total_value.toFixed(2)}</p>
            </div>
            <div className="stat-card">
              <h3>Total Invested</h3>
              <p className="stat-value">€{portfolio.stats.total_invested.toFixed(2)}</p>
            </div>
            <div className="stat-card">
              <h3>Gain/Loss</h3>
              <p className={`stat-value ${portfolio.stats.total_gain_loss >= 0 ? 'positive' : 'negative'}`}>
                €{portfolio.stats.total_gain_loss.toFixed(2)} ({portfolio.stats.total_gain_loss_percentage.toFixed(2)}%)
              </p>
            </div>
          </div>
        )}

        <div className="card">
          <h2>Assets</h2>
          {assets.length === 0 ? (
            <p style={{ textAlign: 'center', color: '#666', padding: '20px' }}>
              No assets in this portfolio. Import transactions or add assets manually.
            </p>
          ) : (
            <table className="table">
              <thead>
                <tr>
                  <th>Symbol</th>
                  <th>Name</th>
                  <th>Type</th>
                  <th>Quantity</th>
                  <th>Avg Price</th>
                  <th>Current Price</th>
                  <th>Value</th>
                  <th>Gain/Loss</th>
                </tr>
              </thead>
              <tbody>
                {assets.map((asset) => (
                  <tr key={asset.id}>
                    <td>
                      <Link to={`/asset/${asset.id}`} style={{ color: '#007bff', textDecoration: 'none' }}>
                        {asset.symbol}
                      </Link>
                    </td>
                    <td>{asset.name}</td>
                    <td>{asset.asset_type}</td>
                    <td>{asset.quantity.toFixed(4)}</td>
                    <td>€{asset.average_buy_price?.toFixed(2) || '-'}</td>
                    <td>€{asset.current_price?.toFixed(2) || '-'}</td>
                    <td>€{asset.stats?.current_value.toFixed(2) || '-'}</td>
                    <td className={asset.stats?.gain_loss >= 0 ? 'positive' : 'negative'}>
                      {asset.stats ? `€${asset.stats.gain_loss.toFixed(2)} (${asset.stats.gain_loss_percentage.toFixed(2)}%)` : '-'}
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

export default PortfolioDetail;
