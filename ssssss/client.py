import grpc
import file_streamer_pb2
import file_streamer_pb2_grpc


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = file_streamer_pb2_grpc.FileStreamerStub(channel)
        request = file_streamer_pb2.FileRequest(filename="example.txt")
        for response in stub.StreamFile(request):
            print(f"Received line: {response.line}")


if __name__ == "__main__":
    run()
