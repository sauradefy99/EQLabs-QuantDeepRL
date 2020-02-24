
const Exchange = require('./lib.js')

const marketId = process.env.MARKET_ID
const market = {
  id: marketId,
  base: 'ETH',
  quote: 'BTC'
}
const queue = process.env.EXCHANGE !== undefined ? process.env.EXCHANGE : 'binance'
const logLevel = process.env.NODE_ENV === 'production' ? 'info' : 'debug'
const rabbitmqAddr = process.env.NODE_ENV === 'production' ? 'amqp://rabbitmq:5672' : 'amqp://localhost:5672'

const exchange = new Exchange(queue, rabbitmqAddr, market, logLevel)

async function startExchange () {
  await exchange.connectToRabbitMq()
  exchange.run()
}

try {
  startExchange()
} catch (err) {
  process.exit(err.code || 1)
}
