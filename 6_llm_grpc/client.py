import grpc
import chat_pb2
import chat_pb2_grpc


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = chat_pb2_grpc.GPTServiceStub(channel)

        try:
            temperature = float(input("Set temperature (e.g., 0.7): "))
        except ValueError:
            temperature = 1.0
            print("Invalid input, using default temperature = 1.0")

        while True:
            try:
                prompt = input("\nEnter your prompt (or type 'exit' to quit): ")
                if prompt.lower() == "exit":
                    print("Goodbye!")
                    break

                print("\n[Response starts streaming...]\n")

                def request_generator():
                    yield chat_pb2.UserPrompt(text=prompt, temperature=temperature)

                for response in stub.Generate(request_generator()):
                    print(response.token, end="", flush=True)

            except KeyboardInterrupt:
                print("\nInterrupted by user. Exiting.")
                break


if __name__ == "__main__":
    run()
