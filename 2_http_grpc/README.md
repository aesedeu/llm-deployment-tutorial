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