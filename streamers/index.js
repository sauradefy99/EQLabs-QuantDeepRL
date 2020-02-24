const amqp = require('amqplib/callback_api');
const ccxws = require("ccxws");
const binance = new ccxws.binance();
let rabbitmq;

const queue = process.env.EXCHANGE !== undefined ? process.env.EXCHANGE : "binance";
const rabbitmqAddr = process.env.RABBIT_MQ_ADDR !== undefined ? process.env.RABBIT_MQ_ADDR : 'rabbitmq:5672';

console.log(queue, rabbitmqAddr);

const market = {
  id: "ETHBTC",
  base: "ETH",
  quote: "BTC",
};

amqp.connect('amqp://' + rabbitmqAddr, (error0, connection) => {
  if (error0) {
    throw error0;
  }
  connection.createChannel((error1, channel) => {
    if (error1) {
      throw error1;
    }

    channel.assertQueue(queue, {
      durable: false
    });

    rabbitmq = channel;
  });
});

binance.on("trade", trade => {
  console.log(trade);
  rabbitmq.sendToQueue(queue, Buffer.from(JSON.stringify(trade)));
});
binance.on("l2snapshot", snapshot => {
  console.log(snapshot);
  rabbitmq.sendToQueue(queue, Buffer.from(JSON.stringify(snapshot)));
});
binance.subscribeTrades(market);
binance.subscribeLevel2Snapshots(market);

