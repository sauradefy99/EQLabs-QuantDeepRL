const L2Streamer = require('./lib.js');

const marketId = process.env.MARKET_ID;
const market = {
  id: marketId,
  base: "ETH",
  quote: "BTC",
};
const queue = process.env.EXCHANGE !== undefined ? process.env.EXCHANGE : "binance";
const logLevel = process.env.NODE_ENV === "production" ? 'info' : 'debug';
const rabbitmqAddr = process.env.NODE_ENV === "production" ? 'amqp://rabbitmq:5672' : 'amqp://localhost:5672';
const websocket = process.env.WEBSOCKET !== "false" ? true : false;

const streamer = new L2Streamer(queue, rabbitmqAddr, market, logLevel);

async function startStreamer() {
  try {
    await streamer.connectToRabbitMq();
    if(websocket) {
      streamer.runWebsocket();
    } else {
      streamer.runPoller(2000);
    }
  } catch (err) {
    throw err
  }
}

try {
  startStreamer();
} catch (err) {
  process.exit(err.code || 1)
}
