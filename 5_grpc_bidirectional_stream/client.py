import grpc
import chat_pb2
import chat_pb2_grpc
import threading
import queue

# Очередь для сообщений, которые пользователь ввёл
message_queue = queue.Queue()


def input_thread(username):
    while True:
        text = input()
        message_queue.put(chat_pb2.ChatMessage(username=username, message=text))


def generate_messages():
    while True:
        msg = message_queue.get()
        yield msg


def receive_messages(stub):
    for msg in stub.Chat(generate_messages()):
        print(f"[{msg.username}] {msg.message}")


if __name__ == "__main__":
    username = input("Enter your username: ")

    channel = grpc.insecure_channel("localhost:50051")
    stub = chat_pb2_grpc.ChatServiceStub(channel)

    # Запускаем поток ввода
    threading.Thread(target=input_thread, args=(username,), daemon=True).start()

    # Получение и отправка сообщений
    receive_messages(stub)
