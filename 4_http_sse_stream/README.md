# Real-time Cryptocurrency Price Stream with FastAPI and SSE

This is a FastAPI application that streams real-time cryptocurrency prices using Server-Sent Events (SSE). It fetches data from Coinbase's public API and provides a console-based client to view the streaming prices.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Service

1. Start the FastAPI server:
```bash
python server.py
```

2. In a separate terminal, run the client:
```bash
python client.py [SYMBOL]
```

For example:
```bash
python client.py BTC-USD  # Stream Bitcoin prices
python client.py ETH-USD  # Stream Ethereum prices
```

If no symbol is provided, it defaults to BTC-USD.

## Features

- Real-time price streaming using Server-Sent Events (SSE)
- Console-based client for viewing price updates
- Fetches data from Coinbase's public API
- Updates every second
- Support for different cryptocurrency pairs (e.g., BTC-USD, ETH-USD, SOL-USD)
- Error handling and automatic reconnection
- Clean console output with timestamps

## Usage

1. Start the server in one terminal
2. Run the client in another terminal
3. Press Ctrl+C to stop the stream 