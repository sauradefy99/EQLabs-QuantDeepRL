import React from 'react';
import logo from './logo.svg';
import './App.css';

const wsBinance = new WebSocket('ws://localhost:8080');
const wsKraken = new WebSocket('ws://localhost:8081');

const App = () => {
  const [binanceOrders, setBinanceOrders] = React.useState({asks: [], bids: []})
  const [krakenOrders, setKrakenOrders] = React.useState({asks: [], bids: []})

  const parseFloats = parsed => {
    return {asks: parsed.asks.map(ask => {return { price: parseFloat(ask.price), size: parseFloat(ask.size)}}), bids: parsed.bids.map(bid => {return { price: parseFloat(bid.price), size: parseFloat(bid.size)}})}
  }

  const minBinance = binanceOrders.bids.reduce((min, bid) => bid.price < min ? bid.price : min, Infinity)
  const minKraken = krakenOrders.bids.reduce((min, bid) => bid.price < min ? bid.price : min, Infinity)

  const maxBinance = binanceOrders.asks.reduce((max, ask) => ask.price > max ? ask.price : max, 0)
  const maxKraken = krakenOrders.asks.reduce((max, ask) => ask.price > max ? ask.price : max, 0)

  const lowestAskBinance = binanceOrders.asks.reduce((min, ask) => ask.price < min ? ask.price : min, Infinity)
  const lowestAskKraken = krakenOrders.asks.reduce((min, ask) => ask.price < min ? ask.price : min, Infinity)

  const highestBidBinance = binanceOrders.bids.reduce((min, bid) => bid.price > min ? bid.price : min, 0)
  const highestBidKraken = krakenOrders.bids.reduce((min, bid) => bid.price > min ? bid.price : min, 0)

  const min = () => {
    return minBinance < minKraken ? minBinance : minKraken
  }

  const max = () => {
    return maxBinance > maxKraken ? maxBinance : maxKraken
  }

  const diff = max() - min();

  React.useEffect(() => {
    wsBinance.onopen = () => {
      console.log("opened connection to binance streamer!");
    }
  
    wsBinance.onmessage = (msg) => {
      const parsed = JSON.parse(msg.data)
      if (parsed.asks.length > 0 && parsed.bids.length > 0) {
        setBinanceOrders(parseFloats(parsed))
      }
    }

    wsKraken.onopen = () => {
      console.log("opened connection to kraken streamer!");
    }
  
    wsKraken.onmessage = (msg) => {
      const parsed = JSON.parse(msg.data)
      if (parsed.asks.length > 0 && parsed.bids.length > 0) {
        setKrakenOrders(parseFloats(parsed))
      }
    }
  },[])


  return (
    <div className="App">
      Min: {min()}
      <br />
      Max: {max()}
      <br />
      Diff: {diff}
      <h1>Binance</h1>
      <div className="bar"><div className="left" style={{width: `${diff / lowestAskBinance * 100}%`}}></div><div className="right" style={{width: `${diff / highestBidBinance * 100}%`}}></div></div>
      <h1>Kraken</h1>
      <div className="bar"><div className="left" style={{width: `${diff / lowestAskKraken * 100}%`}}></div><div className="right" style={{width: `${diff / highestBidKraken * 100}%`}}></div></div>
    </div>
  );
}

export default App;
