const L2Streamer = require('./lib.js')

const marketId = process.env.MARKET_ID
const market = {
  id: marketId,
  base: 'ETH',
  quote: 'BTC'
}
const queue = process.env.EXCHANGE !== undefined ? process.env.EXCHANGE : 'binance'
const logLevel = process.env.NODE_ENV === 'production' ? 'info' : 'debug'
const rabbitmqAddr = process.env.RABBIT_MQ_ADDR !== undefined ? process.env.RABBIT_MQ_ADDR : 'amqp://localhost:5672'
const websocket = process.env.WEBSOCKET !== 'false'
const websocketPort = process.env.OUTGOING_WEBSOCKET_PORT !==undefined ? process.env.OUTGOING_WEBSOCKET_PORT : 8080

const streamer = new L2Streamer(queue, rabbitmqAddr, market, logLevel, websocketPort)

async function startStreamer () {
  await streamer.connectToRabbitMq()
  if (websocket) {
    streamer.runWebsocket()
  } else {
    streamer.runPoller(2000)
  }
}

try {
  startStreamer()
} catch (err) {
  process.exit(err.code || 1)
}
