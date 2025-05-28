import grpc
import llm_pb2, llm_pb2_grpc


def run():
    channel = grpc.insecure_channel("localhost:50051")
    stub = llm_pb2_grpc.LLMServiceStub(channel)

    request = llm_pb2.GenerateRequest(
        prompt="Once upon a time", max_tokens=256, temperature=0.8
    )

    for response in stub.GenerateText(request):
        print(response.token, end="", flush=True)


if __name__ == "__main__":
    run()
