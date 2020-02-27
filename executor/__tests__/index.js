
const path = require("path");
const Exchange = require('../lib.js')

const market = {
  id: "ETH/BTC",
  base: 'ETH',
  quote: 'BTC'
}
const binanceQueue = 'binance'
const krakenQueue = 'kraken'
const logLevel = 'debug'
const rabbitmqAddr = 'amqp://localhost:5672'

const createOrderMessage = Buffer.from(JSON.stringify({
  operation: "create",
  symbol: market.id,
  orderType: "limit",
  side: "buy",
  price: 0.04,
  amount: 0.02
}))

const cancelOrderMessage = Buffer.from(JSON.stringify({
  operation: "cancel",
  symbol: market.id,
  orderId: "5683"
}))

let binance, kraken

describe("Binance tests", () => {
  beforeEach(() => {
    require('dotenv').config({ path: path.resolve('../.binancesecrets') })
    binance = new Exchange(binanceQueue, rabbitmqAddr, market, logLevel)
  });
  
  test('Order creation', async () => {
    const result = await binance.parseMessage(createOrderMessage)
    expect(result.info).toStrictEqual({})
    expect(result.symbol).toBe(market.id)
  });
  
  test('Order cancelation (Can not be actually done, test for error)', async () => {
    const result = await binance.parseMessage(cancelOrderMessage)
    expect(result).toBe(false)
  });
})

describe("Kraken tests", () => {
  beforeEach(() => {
    require('dotenv').config({ path: path.resolve('../.krakensecrets') })
    kraken = new Exchange(krakenQueue, rabbitmqAddr, market, logLevel)
    console.log(kraken.exchange.urls)
  });
  
  test('Order creation', async () => {
    const result = await kraken.parseMessage(createOrderMessage)
    console.log(result)
    expect(result.info).toStrictEqual({})
    expect(result.symbol).toBe(market.id)
  });
  
  test('Order cancelation', async () => {
    const result = await kraken.parseMessage(cancelOrderMessage)
    console.log(result)
    expect(result).toBe(false)
  });
})
