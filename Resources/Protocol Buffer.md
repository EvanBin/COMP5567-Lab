# Protocol Buffer

This tutorial provides a basic Python programmer’s introduction to working with gRPC.

## Defining the service

To define a service, you specify a named `service` in your `.proto` file:

```protobuf
service RouteGuide {
   // (Method definitions not shown)
}
```

Then you define `rpc` methods inside your service definition, specifying their request and response types. gRPC lets you define four kinds of service method, all of which are used in the `RouteGuide` service:

- A *simple RPC* where the client sends a request to the server using the stub and waits for a response to come back, just like a normal function call.

```protobuf
// Obtains the feature at a given position.
rpc GetFeature(Point) returns (Feature) {}
```

Your `.proto` file also contains protocol buffer message type definitions for all the request and response types used in our service methods. You must give each field in your message definition a number between `1` and `536,870,911` ($2^{29}-1$) - for example, here’s the `Point` message type:

```protobuf
message Point {
  int32 latitude = 1;
  int32 longitude = 2;
}
```

## Generating client and server code

Next you need to generate the gRPC client and server interfaces from your `.proto` service definition.

- `--proto_path`: Protocol Path
- `--python_out`: Request and Response Classes
- `--grpc_python_out`: Client and Server Classes

```shell
# This regenerates xx_pb2.py which contains generated request and response classes and xx_pb2_grpc.py which contains generated client and server classes.
python -m grpc_tools.protoc --proto_path=./proto/ --python_out=. --grpc_python_out=. ./proto/blockchain.proto
```
