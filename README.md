# COMP 5567 Lab

Reference: https://grpc.io/



## Prerequisites

- Python 3.7 or higher
- `pip` version 9.0.1 or higher

If necessary, upgrade your version of `pip`:

```shell
$ python -m pip install --upgrade pip
```

Install gRPC and gRPC-tools:

```shell
$ python -m pip install grpcio grpcio-tools
```



## HelloWorld

First, download the example:

```shell
# Clone the repository to get the example code:
$ git clone -b v1.58.0 --depth 1 --shallow-submodules https://github.com/grpc/grpc
# Navigate to the "hello, world" Python example:
$ cd grpc/examples/python/helloworld
```

From the `examples/python/helloworld` directory:

- Run the server

```shell
$ python greeter_server.py
```

- From another terminal, run the client:

```shell
$ python greeter_client.py
```

Congratulations! You’ve just run a client-server application with gRPC.



## Lab 1 - Introduction to gRPC

Now let’s look at how to build a toy blockchain from scratch. Our gRPC service is defined using protocol buffers; you can find out lots more about how to define a service in a `.proto` file in [Introduction to gRPC](https://grpc.io/docs/what-is-grpc/introduction/) and [Basics tutorial](https://grpc.io/docs/languages/python/basics/).

### Edit gRPC Service

You can find the demo `blockchain.proto` in `lab1-grpc/proto/`, which contains two RPC methods: `AddBlock` and `QueryBlock`.

### Generate gRPC code

Next we need to update the gRPC code used by our application to use the new service definition.

From the `lab1-grpc/` directory, run:

```shell
$ python -m grpc_tools.protoc --proto_path=./proto/ --python_out=. --grpc_python_out=. ./proto/blockchain.proto
```

This regenerates `blockchain_pb2.py` which contains our generated request and response classes and `blockchain_pb2_grpc.py` which contains our generated client and server classes.

### Edit and run the application

We now have new generated server and client code, but we still need to implement and call the new method in the human-written parts of our example application. You can find the code from:

- Server: `lab1-grpc/server.py`
- Client (AddBlock): `lab1-grpc/client.py`
- Client (QueryBlock): `lab1-grpc/client_listening.py`

Then you can run the server:

```shell
$ python server.py
```

From another terminal, run the client:

```shell
$ python client.py
# or
$ python client_listening.py
```



# Licence

The MIT License