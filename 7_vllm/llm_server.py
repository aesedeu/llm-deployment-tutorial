import grpc
from concurrent import futures
import json
import requests
import llm_pb2
import llm_pb2_grpc


class LLMService(llm_pb2_grpc.LLMServiceServicer):
    def GenerateText(self, request, context):
        payload = {
            "model": "gpt2",
            "prompt": request.prompt,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "stream": False,  # или True, если хочешь потом стримить
        }

        try:
            response = requests.post(
                "http://localhost:8080/v1/completions", json=payload
            )
            response.raise_for_status()
            result = response.json()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"vLLM error: {e}")
            return

        # отправляем как один ответ (можно переделать на стрим)
        text = result["choices"][0]["text"]
        for token in text:
            yield llm_pb2.GenerateResponse(token=token)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    llm_pb2_grpc.add_LLMServiceServicer_to_server(LLMService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server running on port 50051...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
