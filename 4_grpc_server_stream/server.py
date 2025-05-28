import time
import grpc
from concurrent import futures
import file_streamer_pb2
import file_streamer_pb2_grpc


class FileStreamerServicer(file_streamer_pb2_grpc.FileStreamerServicer):
    def StreamFile(self, request, context):
        filename = request.filename
        try:
            with open(filename, "r") as f:
                for line in f:
                    time.sleep(1)
                    yield file_streamer_pb2.FileLine(line=line.strip())
        except FileNotFoundError:
            context.set_details(f"File {filename} not found")
            context.set_code(grpc.StatusCode.NOT_FOUND)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    file_streamer_pb2_grpc.add_FileStreamerServicer_to_server(
        FileStreamerServicer(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server started on port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
