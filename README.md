# EQLabs-QuantDeepRL

Private repo for the implementation of paper 'Capturing financial markets using deep reinforcement learning': https://arxiv.org/abs/1907.04373 on crypto assets.


## Data flow
1. Streamers stream/poll orders from given exchanges
2. Predictors read the latest order books from the streamers, making predictions and decisions to make or take orders, pushing triggers to executors
3. Executors execute the order events as defined by the predictors

## Running the platform
```bash
make run
```
Stop it:
```bash
make down
```

## Data format
The order book format is loosely defined by `ccxt`, here's an example:
```json
{
  "exchange": "binance",
  "timestamp": 1582555173658,
  "asks": [
    {"price":0.02795,"size":25},
    {"price":0.02796,"size":70.059},
    {"price":0.02798,"size":12.595},
    {"price":0.02799,"size":504},
    {"price":0.028,"size":130.083}
  ],
  "bids": [
    {"price":0.02795,"size":25},
    {"price":0.02796,"size":70.059},
    {"price":0.02798,"size":12.595},
    {"price":0.02799,"size":504},
    {"price":0.028,"size":130.083}
  ],
}
```

Every piece of the puzzle has its message format defined in a `json-schema`, which gets validated before sending to a message queue.
