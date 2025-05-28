import asyncio
import grpc
import time
from grpc_data import model_pb2, model_pb2_grpc

SERVER_ADDRESS = "localhost:50051"
N = 10000


async def call_predict(stub, request_id):
    request = model_pb2.PredictRequest(features=[1.0, 2.0, 3.0])
    response = await stub.Predict(request)
    # Можно закомментировать для тишины
    # print(f"Request {request_id}: Prediction = {response.prediction}")


async def main():
    async with grpc.aio.insecure_channel(SERVER_ADDRESS) as channel:
        stub = model_pb2_grpc.ModelServiceStub(channel)

        start = time.perf_counter()

        tasks = [call_predict(stub, i) for i in range(N)]
        await asyncio.gather(*tasks)

        end = time.perf_counter()
        total_time = end - start
        print(f"\n⚡ Выполнено {N} запросов за {total_time:.2f} секунд")
        print(f"📈 Среднее время на запрос: {total_time / N * 1000:.2f} мс")


if __name__ == "__main__":
    asyncio.run(main())
