import requests
import json
import sys
from datetime import datetime

def stream_prices(symbol: str):
    """Connect to SSE endpoint and display price updates in console"""
    url = f"http://localhost:8000/stream/{symbol}"
    
    print(f"Connecting to price stream for {symbol}...")
    print("Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        with requests.get(url, stream=True) as response:
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    # Skip empty lines and comments
                    if not line or line.startswith(':'):
                        continue
                    
                    # Parse SSE message
                    if line.startswith('data: '):
                        try:
                            data = json.loads(line[6:])  # Remove 'data: ' prefix
                            
                            # Format and display the price update
                            print(f"Symbol: {data['symbol']}")
                            print(f"Price: ${data['price']:.2f}")
                            print(f"Timestamp: {data['timestamp']}")
                            print("-" * 50)
                        except json.JSONDecodeError as e:
                            print(f"Error parsing JSON: {e}")
                            continue
                    
    except KeyboardInterrupt:
        print("\nStopping price stream...")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Default to BTC-USD if no symbol provided
    symbol = sys.argv[1] if len(sys.argv) > 1 else "BTC-USD"
    stream_prices(symbol) 