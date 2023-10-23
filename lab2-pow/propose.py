import logging

import grpc
import blockchain_pb2
import blockchain_pb2_grpc

from concurrent.futures import ThreadPoolExecutor

# Network Information
node_network = ["50051", "50052"]

# Multithread helper function
def proposeHelper(port):
    with grpc.insecure_channel('127.0.0.1:' + port) as channel:
        stub = blockchain_pb2_grpc.BlockChainStub(channel)
        response = stub.ProposeBlock(blockchain_pb2.ProposeBlockRequest())
        print("Client received block address from {}: {}".format(response.node, response.hash))

# The client request the ProposeBlock to server
def run():
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.map(proposeHelper, [port for port in node_network])

if __name__ == '__main__':
    logging.basicConfig()
    run()
