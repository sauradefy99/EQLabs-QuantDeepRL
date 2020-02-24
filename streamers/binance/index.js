const L2Streamer = require('../lib');

const market = {
  id: "ETH/BTC",
  base: "ETH",
  quote: "BTC",
};
const queue = "binance";
const rabbitmqAddr = process.env.NODE_ENV !== "production" ? 'amqp://localhost:5672' : 'amqp://rabbitmq:5672';

const streamer = new L2Streamer(queue, rabbitmqAddr, market, 'debug');

async function startBinanceStreamer() {
  try {
    await streamer.connectToRabbitMq();
    streamer.runWebsocket();
  } catch (err) {
    throw err
  }
}

try {
  startBinanceStreamer();
} catch (err) {
  process.exit(err.code || 1)
}
