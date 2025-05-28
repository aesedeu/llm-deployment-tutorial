import llm_pb2, llm_pb2_grpc
from concurrent import futures
import grpc
import requests
import json


class LLMService(llm_pb2_grpc.LLMServiceServicer):
    def GenerateText(self, request, context):
        # Прокидываем запрос в vLLM API (или другую модель)
        response = requests.post(
            "http://localhost:8080/v1/completions",
            json={
                # "model": "gpt2",
                "model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
                "prompt": request.prompt,
                "max_tokens": request.max_tokens,
                "temperature": request.temperature,
                "stream": True,  # ⚠️ критично
            },
            stream=True,
        )

        for line in response.iter_lines():
            if line:
                line = line.decode("utf-8").strip()
                if line.startswith("data: "):
                    line = line[len("data: "):]

                if line == "[DONE]":
                    break

                try:
                    data = json.loads(line)
                    token = data["choices"][0]["text"]
                    yield llm_pb2.GenerateResponse(token=token)
                except Exception as e:
                    print(f"⚠️ Ошибка парсинга строки: {line}")
                    print(f"❌ {e}")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    llm_pb2_grpc.add_LLMServiceServicer_to_server(LLMService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server running on port 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
