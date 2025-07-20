import React, { useEffect, useState } from 'react'
import axios from 'axios'
import dayjs from 'dayjs' // Add this
import './App.css'

function App() {
  const [trades, setTrades] = useState([])

  useEffect(() => {
    axios.get('https://nifty-coach-backend.onrender.com/get_trades')
      .then(res => {
        setTrades(res.data.trades || res.data || [])  // fallback if `trades` isn't wrapped
      })
      .catch(err => console.error('Error fetching trades:', err))
  }, [])

  return (
    <div className="App">
      <h1>Nifty Trade Coach</h1>
      <table>
        <thead>
          <tr>
            <th>Timestamp</th>
            <th>Symbol</th>
            <th>Side</th>
            <th>Qty</th>
            <th>Price</th>
          </tr>
        </thead>
        <tbody>
          {trades.map((trade, index) => (
            <tr key={index}>
              <td>{dayjs(trade.timestamp).format("YYYY-MM-DD HH:mm:ss")}</td>
              <td>{trade.symbol}</td>
              <td>{trade.side}</td>
              <td>{trade.qty}</td>
              <td>{trade.price}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default App
