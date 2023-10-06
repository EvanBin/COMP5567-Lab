from __future__ import print_function

import logging

import grpc
import blockchain_pb2
import blockchain_pb2_grpc

# The client request the QueryBlock to server, transferring the message by Block data structure
def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = blockchain_pb2_grpc.BlockChainStub(channel)
        response = stub.QueryBlock(blockchain_pb2.QueryBlockRequest())
        print("Client received the current block info: ")
        # Block data structure usage
        print(response.block.data)
        print(response.block.hash)


if __name__ == '__main__':
    logging.basicConfig()
    run()
