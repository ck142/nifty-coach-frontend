
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [trades, setTrades] = useState([]);

  useEffect(() => {
    axios.get("/api/get_trades")
      .then(res => setTrades(res.data.trades || []))
      .catch(err => console.error("Failed to fetch trades:", err));
  }, []);

  const groupedByDate = trades.reduce((acc, trade) => {
    const date = trade.timestamp?.split('T')[0] || "Unknown";
    if (!acc[date]) acc[date] = [];
    acc[date].push(trade);
    return acc;
  }, {});

  return (
    <div className="App">
      <h1>Nifty Trade Coach</h1>
      {Object.entries(groupedByDate).map(([date, dayTrades]) => (
        <div key={date} className="trade-day">
          <h2>{date}</h2>
          <table>
            <thead>
              <tr>
                <th>Symbol</th>
                <th>Side</th>
                <th>Qty</th>
                <th>Price</th>
                <th>P&L</th>
              </tr>
            </thead>
            <tbody>
              {dayTrades.map((trade, idx) => (
                <tr key={idx}>
                  <td>{trade.symbol}</td>
                  <td>{trade.side}</td>
                  <td>{trade.qty}</td>
                  <td>{trade.price}</td>
                  <td>{(trade.pnl || 0).toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}
    </div>
  );
}

export default App;
