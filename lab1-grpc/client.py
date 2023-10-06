from __future__ import print_function

import logging

import grpc
import blockchain_pb2
import blockchain_pb2_grpc

# The client request the AddBlock to server
def run():
    with grpc.insecure_channel('127.0.0.1:50051') as channel:
        stub = blockchain_pb2_grpc.BlockChainStub(channel)
        response = stub.AddBlock(blockchain_pb2.AddBlockRequest(data="test1"))
        print("Client received block address: " + response.hash)


if __name__ == '__main__':
    logging.basicConfig()
    run()
