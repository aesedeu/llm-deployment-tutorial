import grpc
import time
from concurrent import futures
import queue

import chat_pb2
import chat_pb2_grpc


class ChatService(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self):
        self.message_queues = []

    def Chat(self, request_iterator, context):
        q = queue.Queue()
        self.message_queues.append(q)

        username_holder = {"name": None}

        def listen_to_client():
            try:
                for msg in request_iterator:
                    if username_holder["name"] is None:
                        username_holder["name"] = msg.username
                        self.broadcast_system_message(f"{msg.username} вошёл в чат")

                    print(f"[{msg.username}] {msg.message}")
                    self.broadcast(msg, exclude=q)
            except:
                pass
            finally:
                self.message_queues.remove(q)
                if username_holder["name"]:
                    self.broadcast_system_message(
                        f"{username_holder['name']} покинул чат"
                    )

        import threading

        threading.Thread(target=listen_to_client, daemon=True).start()

        while True:
            try:
                msg = q.get(timeout=1)
                yield msg
            except queue.Empty:
                if context.is_active():
                    continue
                else:
                    break

    def broadcast(self, msg, exclude=None):
        for other_q in self.message_queues:
            if other_q != exclude:
                other_q.put(msg)

    def broadcast_system_message(self, text):
        system_msg = chat_pb2.ChatMessage(username="Server", message=text)
        self.broadcast(system_msg)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC chat server started on port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
