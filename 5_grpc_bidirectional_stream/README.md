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