from fastapi import FastAPI
from sse_starlette.sse import EventSourceResponse
import asyncio
import json
import requests
from datetime import datetime

app = FastAPI()

async def fetch_price(symbol: str) -> dict:
    """Fetch price from Coinbase API"""
    try:
        response = requests.get(f'https://api.coinbase.com/v2/prices/{symbol}/spot')
        if response.status_code == 200:
            data = response.json()
            return {
                "symbol": symbol,
                "price": float(data['data']['amount']),
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        print(f"Error fetching price: {e}")
    return None

async def price_generator(symbol: str):
    """Generate price updates"""
    while True:
        price_data = await fetch_price(symbol)
        if price_data:
            yield {
                "event": "price_update",
                "data": json.dumps(price_data)
            }
        await asyncio.sleep(1)

@app.get("/stream/{symbol}")
async def stream_prices(symbol: str):
    """SSE endpoint for streaming prices"""
    return EventSourceResponse(price_generator(symbol))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 