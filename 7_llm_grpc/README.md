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