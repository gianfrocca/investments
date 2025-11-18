import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { assetAPI, transactionAPI } from '../api';

function AssetDetail() {
  const { id } = useParams();
  const [asset, setAsset] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, [id]);

  const fetchData = async () => {
    try {
      const [assetRes, transactionsRes] = await Promise.all([
        assetAPI.get(id),
        transactionAPI.listByAsset(id),
      ]);
      setAsset(assetRes.data);
      setTransactions(transactionsRes.data);
    } catch (err) {
      console.error('Failed to load asset', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading...</div>;
  if (!asset) return <div>Asset not found</div>;

  return (
    <div className="main-content">
      <div className="container">
        <h1>{asset.symbol} - {asset.name}</h1>

        <div className="stats-grid">
          <div className="stat-card">
            <h3>Quantity</h3>
            <p className="stat-value">{asset.quantity.toFixed(4)}</p>
          </div>
          <div className="stat-card">
            <h3>Avg Buy Price</h3>
            <p className="stat-value">€{asset.average_buy_price?.toFixed(2) || '-'}</p>
          </div>
          <div className="stat-card">
            <h3>Current Price</h3>
            <p className="stat-value">€{asset.current_price?.toFixed(2) || '-'}</p>
          </div>
          <div className="stat-card">
            <h3>Total Value</h3>
            <p className="stat-value">€{asset.stats?.current_value.toFixed(2) || '-'}</p>
          </div>
        </div>

        <div className="card">
          <h2>Transaction History</h2>
          {transactions.length === 0 ? (
            <p style={{ textAlign: 'center', color: '#666' }}>No transactions</p>
          ) : (
            <table className="table">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Type</th>
                  <th>Quantity</th>
                  <th>Price</th>
                  <th>Total</th>
                  <th>Fees</th>
                </tr>
              </thead>
              <tbody>
                {transactions.map((tx) => (
                  <tr key={tx.id}>
                    <td>{new Date(tx.transaction_date).toLocaleDateString()}</td>
                    <td>{tx.transaction_type}</td>
                    <td>{tx.quantity}</td>
                    <td>€{tx.price_per_unit.toFixed(2)}</td>
                    <td>€{tx.total_amount.toFixed(2)}</td>
                    <td>€{tx.fees.toFixed(2)}</td>
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

export default AssetDetail;
