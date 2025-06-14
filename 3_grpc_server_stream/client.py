import grpc
import price_service_pb2
import price_service_pb2_grpc
import time

def run():
    # Create a gRPC channel
    with grpc.insecure_channel('localhost:50051') as channel:
        # Create a stub (client)
        stub = price_service_pb2_grpc.PriceServiceStub(channel)
        
        # Create a request
        request = price_service_pb2.PriceRequest(symbol='BTC-USD')
        
        try:
            # Start streaming
            print("Starting to receive price updates...")
            for response in stub.StreamPrices(request):
                print(f"Symbol: {response.symbol}")
                print(f"Price: ${response.price:.2f}")
                print(f"Timestamp: {response.timestamp}")
                print("-" * 50)
                
        except KeyboardInterrupt:
            print("\nStopping client...")
        except grpc.RpcError as e:
            print(f"RPC Error: {e}")

if __name__ == '__main__':
    run() 