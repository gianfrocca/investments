import React, { useState, useEffect } from 'react';
import { portfolioAPI, importAPI } from '../api';

function Import() {
  const [portfolios, setPortfolios] = useState([]);
  const [selectedPortfolio, setSelectedPortfolio] = useState('');
  const [importType, setImportType] = useState('trade-republic');
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchPortfolios();
  }, []);

  const fetchPortfolios = async () => {
    try {
      const response = await portfolioAPI.list();
      setPortfolios(response.data);
      if (response.data.length > 0) {
        setSelectedPortfolio(response.data[0].id);
      }
    } catch (err) {
      setError('Failed to load portfolios');
    }
  };

  const handleSubmit = async (e) => {
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
      let response;
      if (importType === 'trade-republic') {
        response = await importAPI.tradeRepublic(selectedPortfolio, file);
      } else {
        response = await importAPI.generic(selectedPortfolio, file);
      }

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
        <h1>Import Transactions</h1>

        <div className="card">
          <h2>Import from CSV</h2>

          {error && <div className="error">{error}</div>}
          {result && (
            <div className="success">
              Import completed! Imported: {result.imported}, Skipped: {result.skipped}
              {result.errors.length > 0 && <div>Errors: {result.errors.join(', ')}</div>}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Select Portfolio</label>
              <select
                value={selectedPortfolio}
                onChange={(e) => setSelectedPortfolio(e.target.value)}
                required
              >
                {portfolios.map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Import Type</label>
              <select value={importType} onChange={(e) => setImportType(e.target.value)}>
                <option value="trade-republic">Trade Republic</option>
                <option value="generic">Generic CSV</option>
              </select>
            </div>

            <div className="form-group">
              <label>CSV File</label>
              <input type="file" accept=".csv" onChange={(e) => setFile(e.target.files[0])} required />
            </div>

            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? 'Importing...' : 'Import'}
            </button>
          </form>
        </div>

        <div className="card">
          <h2>CSV Format Help</h2>
          <p><strong>Trade Republic format:</strong></p>
          <pre style={{ background: '#f5f5f5', padding: '10px', borderRadius: '5px', overflow: 'auto' }}>
            Date,Time,Type,Symbol,ISIN,Quantity,Price,Total,Currency,Notes
          </pre>

          <p style={{ marginTop: '20px' }}><strong>Generic format:</strong></p>
          <pre style={{ background: '#f5f5f5', padding: '10px', borderRadius: '5px', overflow: 'auto' }}>
            date,symbol,name,type,quantity,price,fees,currency
          </pre>
        </div>
      </div>
    </div>
  );
}

export default Import;
