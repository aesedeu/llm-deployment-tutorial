### 12 vLLM -> Websocket -> gRPC -> Web UI (`12_vllm_grpc_websocket/`)

```bash
python3 -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2.5-0.5B-Instruct \
    --port 8080 \
    --tensor-parallel-size 1 \
    --max-num-seqs 16 \
    --max-num-batched-tokens 32768 \
    --trust-remote-code

docker compose up -d
python llm_server.py
```

Now create requests via Web UI