### 8. Run vLLM /v1/completions with gRPC (`8_vllm_grpc/`)
Implementation using vLLM for optimized LLM serving:
- vLLM API server setup
- Integration with popular LLM models (e.g., GPT-2, TinyLlama)
- Streaming completion endpoints
- Performance optimization settings
- gRPC client-server architecture for vLLM
- Web interface with Nginx reverse proxy
- Docker Compose deployment setup
- Prometheus monitoring integration

Setup and running:

1. Basic vLLM setup:
```bash
# Install vLLM with gRPC support
pip install "vllm[grpc]"

# Start vLLM server with GPT-2
python3 -m vllm.entrypoints.openai.api_server \
    --model gpt2 \
    --port 8081 \
    --tensor-parallel-size 1

# Or start with TinyLlama
python3 -m vllm.entrypoints.openai.api_server \
    --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 \
    --port 8080 \
    --tensor-parallel-size 1 \
    --max-num-seqs 16 \
    --max-num-batched-tokens 4096 \
    --trust-remote-code
```

2. Docker Compose deployment:
```bash
# Start the entire stack
docker-compose up -d
```

The Docker Compose setup includes:
- Nginx reverse proxy (port 80)
- vLLM service (port 8080)
- Prometheus monitoring (port 9090)
- Grafana dashboard (port 3000)

Nginx configuration provides:
- Static web interface serving
- Reverse proxy to vLLM API
- Proper handling of streaming responses
- CORS and security headers

Web Interface Features:
- MVP chat interface
- Real-time streaming responses
- Adjustable temperature and max tokens

Testing the deployment:
```bash
# Test model availability
curl http://localhost:8080/v1/models

# Check metrics
curl http://localhost:8080/metrics

# Test completion endpoint
# CLI request directly to vLLM endpoint
curl http://localhost:8080/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    "prompt": "Hello",
    "max_tokens": 100
  }'

curl http://localhost:8080/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    "prompt": "Hello",
    "max_tokens": 100,
    "stream": true
  }'

# CLI request to gRPC
python llm_server.py
python llm_client.py
```

**Architecture flow with CLI:**
```
gRPC client (llm_client.py)
        │
        ▼
gRPC server (llm_server_streaming.py)
        │
        ▼
vLLM API server (localhost:8080/v1/completions)
        │
        ▼
[ tokens arrive gradually ]
        │
        ▼
gRPC server reads tokens and sends to client via stream
        │
        ▼
gRPC client prints them to console as they arrive
```

**Architecture flow with Web UI:**
```
Web UI (nginx static HTML + JS)
        │
        ▼
vLLM API server (localhost:8080/v1/completions)
        │
        ▼
[ tokens arrive gradually ]
        │
        ▼
Web UI server reads tokens and sends to client via stream
```