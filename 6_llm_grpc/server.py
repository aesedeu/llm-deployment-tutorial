import grpc
from concurrent import futures
import time

import chat_pb2
import chat_pb2_grpc

from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch


class GPTService(chat_pb2_grpc.GPTServiceServicer):
    def __init__(self):
        print("Loading model...")
        self.device = torch.device(
            "cuda"
            if torch.cuda.is_available()
            else "mps" if torch.backends.mps.is_available() else "cpu"
        )

        self.model = GPT2LMHeadModel.from_pretrained("gpt2").to(self.device)
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        self.model.eval()
        print(f"Model loaded. to {self.device}")

    def Generate(self, request_iterator, context):
        for user_prompt in request_iterator:
            temperature = max(0.1, min(user_prompt.temperature, 2.0))  # clamp value
            input_ids = self.tokenizer.encode(user_prompt.text, return_tensors="pt").to(self.device)
            output_ids = input_ids.clone()

            for _ in range(50):
                with torch.no_grad():
                    outputs = self.model(output_ids)
                    next_token_logits = outputs.logits[:, -1, :] / temperature
                    next_token_id = torch.argmax(next_token_logits, dim=-1).unsqueeze(0)
                    output_ids = torch.cat([output_ids, next_token_id], dim=-1)

                token_str = self.tokenizer.decode(next_token_id.squeeze())
                yield chat_pb2.GeneratedToken(token=token_str)
                time.sleep(0.1)
            break


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_GPTServiceServicer_to_server(GPTService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server started at port 50051.")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
