const amqp = require('amqplib/callback_api');
const ccxt = require('ccxt');

(async function () {
  const binance  = new ccxt.binance({ enableRateLimit: true })
  const orderBook = await binance.fetchL2OrderBook()

  amqp.connect('amqp://rabbitmq:5672', function(error0, connection) {});
  amqp.connect('amqp://rabbitmq:5672', function(error0, connection) {
  if (error0) {
    throw error0;
  }
  connection.createChannel(function(error1, channel) {});
  });
  amqp.connect('amqp://rabbitmq:5672', function(error0, connection) {
    if (error0) {
      throw error0;
    }
    connection.createChannel(function(error1, channel) {
      if (error1) {
        throw error1;
      }
      const queue = 'hello';
      const msg = 'Hello world';

      channel.assertQueue(queue, {
        durable: false
      });

      channel.sendToQueue(queue, Buffer.from(msg));
      console.log(" [x] Sent %s", msg);
    });
  });
})

