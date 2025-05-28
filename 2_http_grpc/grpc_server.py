import grpc
from concurrent import futures
from grpc_data import model_pb2
from grpc_data import model_pb2_grpc
import time
import joblib  # или другая библиотека загрузки модели

# Загружаем модель
model = joblib.load("model.joblib")  # Например, sklearn-модель


class ModelService(model_pb2_grpc.ModelServiceServicer):
    def Predict(self, request, context):
        print(f"[gRPC] Получен запрос с признаками: {request.features}")
        features = [request.features]
        prediction = model.predict(features)[0]
        print(f"[gRPC] Ответ: {prediction}")
        return model_pb2.PredictResponse(prediction=prediction)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    model_pb2_grpc.add_ModelServiceServicer_to_server(ModelService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server started on port 50051.")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()
