import grpc
from concurrent import futures
import time
import os

import chat_pb2
import chat_pb2_grpc

from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import signal
import sys


class GPTService(chat_pb2_grpc.GPTServiceServicer):
    def __init__(self):
        print("Loading model...")
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        self.model = GPT2LMHeadModel.from_pretrained("gpt2")
        self.model.eval()
        print("Model loaded.")

    def Generate(self, request_iterator, context):
        for user_prompt in request_iterator:
            input_ids = self.tokenizer.encode(user_prompt.text, return_tensors="pt")
            output_ids = input_ids.clone()

            for _ in range(50):
                with torch.no_grad():
                    outputs = self.model(output_ids)
                    next_token_logits = outputs.logits[:, -1, :]
                    next_token_id = torch.argmax(next_token_logits, dim=-1).unsqueeze(0)
                    output_ids = torch.cat([output_ids, next_token_id], dim=-1)

                token_str = self.tokenizer.decode(next_token_id.squeeze())
                yield chat_pb2.GeneratedToken(token=token_str)
                time.sleep(0.1)
            break


def serve():
    # fix for macOS fork bug with PyTorch
    import multiprocessing as mp

    mp.set_start_method("spawn", force=True)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    chat_pb2_grpc.add_GPTServiceServicer_to_server(GPTService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server started at port 50051.")
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Shutting down gracefully")
        server.stop(0)
        sys.exit(0)


if __name__ == "__main__":
    serve()
