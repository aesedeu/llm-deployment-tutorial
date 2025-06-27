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