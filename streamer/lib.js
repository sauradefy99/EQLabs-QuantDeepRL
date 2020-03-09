const amqp = require('amqplib/callback_api');
const winston = require('winston');
const ccxws = require('ccxws');
const ccxt = require('ccxt');
const Ajv = require('ajv');
const WebSocket = require('ws');

const ajv = new Ajv()
const schema = require('./schema.json')
const validate = ajv.compile(schema)

class L2Streamer {
  constructor (exchange, rabbitMqHostAddr, market, logLevel, websocketPort) {
    this.logger = winston.createLogger({
      level: logLevel || 'info',
      defaultMeta: { service: 'streamer-' + exchange },
      transports: [
        new winston.transports.Console({
          format: winston.format.json()
        })
      ]
    })

    this.queue = exchange
    this.rabbitMqHostAddr = rabbitMqHostAddr
    this.market = market

    this.streamingExchange = new ccxws[exchange]()
    this.exchange = new ccxt[exchange]({
      enableRateLimit: true
    })
    this.rabbitmq = undefined
    
    this.ws = undefined
    this.wss = new WebSocket.Server({ port: websocketPort });
    
    this.wss.on('connection', (ws) => {
      this.ws = ws
      this.logger.info("A new websocket client connected!")
    });

    this.logger.info('Streamer started on queue: ', this.queue, this.rabbitMqHostAddr)
  }

  wait (duration) {
    return new Promise(resolve => {
      setTimeout(resolve, duration)
    })
  }

  prepareL2SnapshotForSending (snapshot) {
    snapshot.asks = snapshot.asks.map(point => {
      if (point.length === undefined) {
        return { price: point.price, size: point.size }
      }
      return { price: point[0], size: point[1] }
    })
    snapshot.bids = snapshot.bids.map(point => {
      if (point.length === undefined) {
        return { price: point.price, size: point.size }
      }
      return { price: point[0], size: point[1] }
    })
    snapshot.timestamp = Date.now()
    snapshot.quote = this.market.quote;
    snapshot.base = this.market.base;
    snapshot.exchange = this.queue;
    if (!validate(snapshot)){
      this.logger.error(validate.errors);
      return false
    } else {
      const snapshotString = JSON.stringify(snapshot)
      this.logger.debug('Snapshot received: ' + snapshotString)
      return snapshotString
    }
  }

  async connectToRabbitMq () {
    return new Promise((resolve, reject) => {
      amqp.connect(this.rabbitMqHostAddr, (error0, connection) => {
        if (error0 || !connection) {
          this.logger.error('Connection to RabbitMQ failed: ' + error0)
          reject(error0)
        }
        this.logger.info('Successfully connected to rabbitmq')
        connection.createChannel((error1, channel) => {
          if (error1) {
            this.logger.error('Creating a channel on RabbitMQ failed: ' + error1)
            reject(error1)
          }

          channel.assertQueue(this.queue, {
            autoDelete: false,
            durable: false,
            arguments: {
              'x-message-ttl': 20000
            }
          })

          this.logger.info('Successfully created a message queue: ' + this.queue)
          this.rabbitmq = channel

          resolve(true)
        })
      })
    })
  }

  runWebsocket () {
    this.streamingExchange.on('l2snapshot', snapshot => {
      const data = this.prepareL2SnapshotForSending(snapshot)
      if(data) {
        this.rabbitmq.sendToQueue(this.queue, Buffer.from(data))
        this.wss.clients.forEach(client => {
          if (client.readyState === WebSocket.OPEN) {
            client.send(data);
          }
        });
      }
    })
    this.streamingExchange.on('trade', trade => {
      console.log(trade)
    })
    this.streamingExchange.subscribeLevel2Snapshots(this.market)
    this.streamingExchange.subscribeTrades(this.market)
  }

  async runPoller (interval) {
    while (true) {
      try {
        const snapshot = await this.exchange.fetchL2OrderBook(this.market.id)
        const trades = await this.exchange.fetchTrades(this.market.id)
        console.log(trades)
        const data = this.prepareL2SnapshotForSending(snapshot)
        if(data) {
          this.rabbitmq.sendToQueue(this.queue, Buffer.from(data))
          this.wss.clients.forEach(client => {
            if (client.readyState === WebSocket.OPEN) {
              client.send(data);
            }
          });
        }
      } catch (e) {
        this.logger.error(e)
        throw e
      }
      await this.wait(interval)
    }
  }
}

module.exports = L2Streamer
