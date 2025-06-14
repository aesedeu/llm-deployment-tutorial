import grpc
from concurrent import futures
import time
import json
import requests
from datetime import datetime
import price_service_pb2
import price_service_pb2_grpc

class PriceServiceServicer(price_service_pb2_grpc.PriceServiceServicer):
    def StreamPrices(self, request, context):
        symbol = request.symbol
        while True:
            try:
                # Fetch real-time price from Coinbase API
                response = requests.get(f'https://api.coinbase.com/v2/prices/{symbol}/spot')
                if response.status_code == 200:
                    data = response.json()
                    price = float(data['data']['amount'])
                    
                    # Create and yield the response
                    price_response = price_service_pb2.PriceResponse(
                        symbol=symbol,
                        price=price,
                        timestamp=datetime.now().isoformat()
                    )
                    yield price_response
                
                # Wait for 1 second before next update
                time.sleep(1)
                
            except Exception as e:
                print(f"Error fetching price: {e}")
                time.sleep(1)
                continue

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    price_service_pb2_grpc.add_PriceServiceServicer_to_server(
        PriceServiceServicer(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve() 