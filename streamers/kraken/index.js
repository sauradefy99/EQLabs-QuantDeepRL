const L2Streamer = require('../lib');

const market = {
  id: "ETH/BTC",
  base: "ETH",
  quote: "XBT",
};
const queue = "kraken";
const rabbitmqAddr = process.env.NODE_ENV !== "production" ? 'amqp://localhost:5672' : 'amqp://rabbitmq:5672';

const streamer = new L2Streamer(queue, rabbitmqAddr, market, 'debug');

async function startKrakenStreamer() {
  try {
    await streamer.connectToRabbitMq();
    streamer.runPoller(2000);
  } catch (err) {
    throw err
  }
}

try {
  startKrakenStreamer();
} catch (err) {
  process.exit(err.code || 1)
}
