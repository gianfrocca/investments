import React, { useState } from 'react';
import { backupAPI } from '../api';

function Backup() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleExport = async () => {
    try {
      const response = await backupAPI.exportAll();
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `investment_backup_${Date.now()}.json`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      setError('Failed to export data');
    }
  };

  const handleImport = async (e) => {
    e.preventDefault();
    setError('');
    setResult(null);
    setLoading(true);

    if (!file) {
      setError('Please select a file');
      setLoading(false);
      return;
    }

    try {
      const response = await backupAPI.import(file);
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Import failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="main-content">
      <div className="container">
        <h1>Backup & Restore</h1>

        <div className="card">
          <h2>Export Data</h2>
          <p>Download all your portfolio data as a JSON file. You can use this as a backup or to migrate to another instance.</p>
          <button onClick={handleExport} className="btn btn-primary">
            📥 Download Backup
          </button>
        </div>

        <div className="card">
          <h2>Import Data</h2>
          <p>Restore your data from a backup file. This will create new portfolios, assets, and transactions.</p>

          {error && <div className="error">{error}</div>}
          {result && (
            <div className="success">
              Import completed!
              <br />
              Portfolios: {result.portfolios_imported}
              <br />
              Assets: {result.assets_imported}
              <br />
              Transactions: {result.transactions_imported}
            </div>
          )}

          <form onSubmit={handleImport}>
            <div className="form-group">
              <label>Backup File (JSON)</label>
              <input type="file" accept=".json" onChange={(e) => setFile(e.target.files[0])} required />
            </div>

            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? 'Importing...' : '📤 Restore Backup'}
            </button>
          </form>
        </div>

        <div className="card" style={{ background: '#fff3cd', border: '1px solid #ffc107' }}>
          <h3 style={{ margin: '0 0 10px 0' }}>⚠️ Important Notes</h3>
          <ul style={{ margin: 0, paddingLeft: '20px' }}>
            <li>Backup files contain all your portfolio data including transactions and price history</li>
            <li>Importing will create NEW portfolios - it won't update existing ones</li>
            <li>Store backup files securely as they contain your financial data</li>
            <li>Regular backups are recommended to prevent data loss</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default Backup;
