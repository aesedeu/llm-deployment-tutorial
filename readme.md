# LLM Deployment Examples

This repository contains a collection of examples demonstrating different approaches to deploying Large Language Models (LLMs) and ML models in production. Each folder contains a specific example focusing on different deployment aspects and technologies.

## Repository Structure

### 1. Docker Basics (`1_introduce_docker/`)
Introduction to containerization for ML models:
- Basic Docker setup for ML applications
- Best practices for containerizing ML models
- Foundation for more complex deployment scenarios

```bash
# simple nginx with static
docker run -it --rm -p 80:80 nginx:latest
docker run -it --rm -p 80:80 -v ./nginx_container_1/index.html:/usr/share/nginx/html/index.html nginx:latest

# nginx as load balancer
docker network create nginx_network
docker run -d --name nginx_static_1 --network nginx_network -v ./nginx_container_1/index.html:/usr/share/nginx/html/index.html nginx:latest
docker run -d --name nginx_static_2 --network nginx_network -v ./nginx_container_2/index.html:/usr/share/nginx/html/index.html nginx:latest
docker run -d --name nginx_balancer --network nginx_network -p 80:80 -v ./nginx_balancer/nginx.conf:/etc/nginx/nginx.conf nginx:latest

# or docker compose
docker compose up -d
```

### 2. HTTP and gRPC Implementation (`2_http_grpc/`)
Demonstrates two common API implementation approaches:
- HTTP server implementation for model serving
- gRPC server implementation with protobuf
- Comparison between HTTP and gRPC approaches
- Includes example client implementations and testing scripts
- Jupyter notebook for model development and testing

Running the example:
1. Generate gRPC code from protobuf
2. Start the server (either HTTP or gRPC)
3. Test using the provided notebook or Postman (for gRPC, include the `model.proto` file and specify ModelService + Message)

```bash
# Create gRPC protobuf-files
cd grpc_data
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. model.proto

# Run HTTP server
python http_server.py

# Run gRPC server
python grpc_server.py
```


### 3. gRPC Server Streaming (`3_grpc_server_stream/`)
Implementation of server-side streaming with gRPC:
- Demonstrates handling large file transfers
- Server-side streaming patterns
- Protobuf definitions for streaming services

```bash
python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. ./proto/price_service.proto
python server.py
python client.py
```

### 4. gRPC Server Streaming (`4_http_sse_stream/`)
```bash
python server.py
python client.py BTC-USD  # Stream Bitcoin prices
python client.py ETH-USD  # Stream Ethereum prices
```

### 5. Bidirectional gRPC Streaming (`5_grpc_bidirectional_stream/`)
Advanced gRPC streaming implementation:
- Bidirectional streaming between client and server
- Chat-like application example
- Real-time communication patterns

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. chat.proto
python server.py

# terminal 1:
python client.py
# terminal 2:
python client.py
```


### 6. NVIDIA Triton Server (`6_triton/`)
Integration with NVIDIA Triton Inference Server:
- Model deployment using Triton server
- Support for multiple model formats (ONNX, TensorRT)
- Performance monitoring with Grafana and Prometheus
- Model optimization examples
- FastAPI integration for serving models

**Models list (`triton/models`)**:
- classic_model
- bert_model
- gpt2_model

Setup and running:
1. Move `triton/bert_trt` to `triton/models` (requires NVIDIA GPU)
2. Import Grafana dashboard from `dash-grafana-triton.json`
3. Create models in `research.ipynb` and move to `triton/models/classic_model`
4. Start the project:
```bash
# after this command be sure that all the models successfully loaded to triton (see container logs)
docker compose up -d
```

5. For TensorRT conversion:
```bash
# Enter TensorRT container
docker exec -it trtexec_container bash

# Convert ONNX to TensorRT
trtexec \
    --onnx=model.onnx \
    --saveEngine=model.plan \
    --minShapes=input:1x3 \
    --optShapes=input:8x3 \
    --maxShapes=input:16x3 \
    --fp16 \
    --useSpinWait
```
6. Start FastAPI server:
```bash
python app.py
```
7. Check the availability via .ipynb file attached in the folder. There're a couple examples how to try triton via HTTP protocol.
8. Visit grafana dashboard (don't forget to create connection to Prometheus) to see metrics.
9. Try locust to see how dynamic batching works.



### 7. LLM with gRPC (`7_llm_grpc/`)
Integration of LLMs with gRPC:
- LLM-specific gRPC service implementation
- Support for both CUDA and CPU deployments
- Optimized for machine learning model serving
- Protobuf definitions for LLM services


```bash
# Generate gRPC code
python -m grpc_tools.protoc -I=proto --python_out=. --grpc_python_out=. proto/chat.proto

# Start server
python server.py

# Start server on macOS (if any troubles with the previous command)
OMP_NUM_THREADS=1 python server.py

# Try CLI client
python client.py
```

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

### 9 OpenVINO
TODO

### 10 Run vLLM /v1/chat/completions with SSE FastAPI  (`10_vllm_sse_fastapi/`)
```bash
# tinyllama
python3 -m vllm.entrypoints.openai.api_server \
    --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 \
    --port 8080 \
    --tensor-parallel-size 1 \
    --max-num-seqs 16 \
    --max-num-batched-tokens 4096 \
    --trust-remote-code

python server.py # run on 8001

# запрос на сервер FastAPI
curl -N -X POST http://localhost:8001/stream \
     -H "Content-Type: application/json" \
     -d '{
        "model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        "message": "Who are you?",
        "max_tokens": 100,
        "temperature": 0.9
        }'
```

```bash
# qwen
# 0.5B
python3 -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2.5-0.5B-Instruct \
    --port 8080 \
    --tensor-parallel-size 1 \
    --max-num-seqs 16 \
    --max-num-batched-tokens 32768 \
    --trust-remote-code

# 7B
python3 -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2.5-7B-Instruct \
    --port 8080 \
    --tensor-parallel-size 1 \
    --max-num-seqs 16 \
    --max-num-batched-tokens 32768 \
    --trust-remote-code

# Запрос из консоли
curl http://localhost:8080/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen2.5-0.5B-Instruct",
    "prompt": "Hello",
    "max_tokens": 100
  }'

# запрос на сервер FastAPI
curl -N -X POST http://localhost:8001/stream \
     -H "Content-Type: application/json" \
     -d '{
        "model": "Qwen/Qwen2.5-0.5B-Instruct",
        "message": "Who is your creator?",
        "max_tokens": 100,
        "temperature": 0.9
        }'

curl -N -X POST http://localhost:8001/stream \
     -H "Content-Type: application/json" \
     -d '{
        "model": "Qwen/Qwen2.5-0.5B-Instruct",
        "message": "How to cook apple pie?",
        "max_tokens": 100,
        "temperature": 1
        }'

curl -N -X POST http://localhost:8001/stream \
     -H "Content-Type: application/json" \
     -d '{
        "model": "Qwen/Qwen2.5-7B-Instruct",
        "message": "How to cook apple pie?",
        "max_tokens": 100,
        "temperature": 1
        }'
```

### 11 Triton vLLM backend
<!-- ```bash
https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/tutorials/Quick_Deploy/vLLM/README.html

wget -P model_repository/vllm_model/1 https://raw.githubusercontent.com/triton-inference-server/vllm_backend/refs/heads/main/samples/model_repository/vllm_model/1/model.json
wget -P model_repository/vllm_model/ https://raw.githubusercontent.com/triton-inference-server/vllm_backend/refs/heads/main/samples/model_repository/vllm_model/config.pbtxt

docker run -it --net=host --rm \
  -p 8001:8001 \
  --shm-size=1G \
  --ulimit memlock=-1 \
  --ulimit stack=67108864 \
  -v ${PWD}:/work \
  -w /work \
  nvcr.io/nvidia/tritonserver:25.05-vllm-python-py3 \
  tritonserver --model-store ./model_repository

docker run -it --net=host -v ${PWD}:/workspace/ nvcr.io/nvidia/tritonserver:25.05-py3-sdk bash
```

## Target Audience

This repository is designed for ML engineers who want to learn about:
- Production deployment of LLMs and ML models
- Different serving architectures (HTTP, gRPC, Triton)
- Streaming and real-time inference
- Performance optimization techniques
- Container-based deployment
- Modern API design patterns

## Prerequisites

- Basic understanding of Python and ML concepts
- Docker installed for containerization examples
- NVIDIA GPU (optional, for GPU-accelerated examples)
- Understanding of API concepts (REST, gRPC) -->

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