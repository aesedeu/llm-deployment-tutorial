# Real-time Price Streaming gRPC Service

This is a gRPC service that streams real-time cryptocurrency prices from Coinbase's public API.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Generate the gRPC code from the proto file:
```bash
python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. ./proto/price_service.proto
```

## Running the Service

1. Start the gRPC server:
```bash
python server_web.py
```

2. In a separate terminal, run the client:
```bash
python client.py
```

The client will start receiving real-time price updates for BTC-USD. You can modify the symbol in the client code to receive prices for other cryptocurrencies (e.g., 'ETH-USD', 'SOL-USD', etc.).

## Features

- Real-time price streaming using gRPC
- Fetches data from Coinbase's public API
- Updates every second
- Error handling and automatic reconnection
- Support for different cryptocurrency pairs 