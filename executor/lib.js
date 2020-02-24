const amqp = require('amqplib/callback_api')
const winston = require('winston')
const ccxt = require('ccxt')

class Exchange {
  constructor (exchange, rabbitMqHostAddr, market, logLevel) {
    this.queue = exchange
    this.rabbitMqHostAddr = rabbitMqHostAddr
    this.market = market
    this.exchange = new ccxt[exchange]({
      enableRateLimit: true
    })
    this.rabbitmq = undefined

    this.logger = winston.createLogger({
      level: logLevel || 'info',
      defaultMeta: { service: 'executor-' + exchange },
      transports: [
        new winston.transports.Console({
          format: winston.format.json()
        })
      ]
    })

    this.logger.info('Executor started on queue: ', this.queue, this.rabbitMqHostAddr)
  }

  wait (duration) {
    return new Promise(resolve => {
      setTimeout(resolve, duration)
    })
  }

  async connectToRabbitMq () {
    return new Promise((resolve, reject) => {
      amqp.connect(this.rabbitMqHostAddr, (error0, connection) => {
        if (error0) {
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

  run () {
    this.rabbitmq.consume(this.queue, (msg) => {
      console.log(msg.content.toString())
    }, {
      noAck: true
    })
  }
}

module.exports = Exchange
