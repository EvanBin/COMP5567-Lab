import sys
import json
import logging

import random
import hashlib

import grpc
import blockchain_pb2
import blockchain_pb2_grpc

from concurrent.futures import ThreadPoolExecutor

BREAK_LINE = "=================================================="

# Network Information
# command line argument: port, node name
node_name = sys.argv[2]
node_network = ["50051", "50052"]

# Blockchain Information
blockchain_height = 0
blockchain_dict = {}

# gRPC Server
class Blockchain(blockchain_pb2_grpc.BlockChainServicer):

    def AddBlock(self, request, context):
        print(BREAK_LINE)
        print("Request: AddBlock()")
        
        # use global because these will be changed inside func
        global blockchain_dict
        global blockchain_height
        
        # prev hash
        prev_hash = ""
        if blockchain_height > 0:
            prev_hash = blockchain_dict[blockchain_height-1]["hash"]
        
        # current hash = prev hash + current data
        data = prev_hash + request.data
        
        # hash code generation, used for block address
        hash_code = hashlib.sha3_256(data.encode("utf-8")).hexdigest()
        
        # store the data and address at blockchain
        blockchain_dict[blockchain_height] = {
            "hash": hash_code,
            "data": request.data
        }
        
        # height growth
        blockchain_height += 1
        
        print(json.dumps(blockchain_dict, indent=2))
        print(BREAK_LINE)
        return blockchain_pb2.AddBlockResponse(hash=hash_code)

    def QueryBlock(self, request, context):
        print(BREAK_LINE)
        print("Request: QueryBlock()")
        
        self_block = blockchain_pb2.Block(
            height=blockchain_height-1,
            hash=blockchain_dict[blockchain_height-1]["hash"],
            data=blockchain_dict[blockchain_height-1]["data"]
        )
        
        print(BREAK_LINE)
        return blockchain_pb2.QueryBlockResponse(block=self_block)
    
    def ProposeBlock(self, request, context):
        print(BREAK_LINE)
        print("Request: ProposeBlock()")
        
        # use global because these will be changed inside func
        global blockchain_dict
        global blockchain_height
        
        # proof-of-work
        current_height = blockchain_height
        print("Current Height: {}".format(current_height))
        nonce = random.randint(0, 2**18)
        print("Proposing block start with nonce: {}".format(nonce))
        
        # prev hash
        prev_hash = ""
        if blockchain_height > 0:
            prev_hash = blockchain_dict[blockchain_height-1]["hash"]
        
        while True:
            # block message = prev hash + node name + nonce
            guess = prev_hash + node_name + "_" + str(nonce)
            guess_hash = hashlib.sha3_256(str.encode(guess)).hexdigest()
            # difficulty fixed to "00000"
            if guess_hash.startswith("00000"):
                print("Block Hash: {}".format(guess_hash))
                print("Nonce: {}".format(nonce))
                break
            nonce += 1
        
        # check block height
        # print("Height {}:{}".format(blockchain_height, current_height))
        if blockchain_height > current_height:
            print("Failed to propose the block.")
            guess_hash = "FAIL"
        else:
            # update local record
            data = node_name + "_" + str(nonce)
            blockchain_dict[blockchain_height] = {
                "hash": guess_hash,
                "data": data
            }
            blockchain_height += 1
            
            # broadcast result
            for port in node_network:
                with grpc.insecure_channel('127.0.0.1:' + port) as channel:
                    stub = blockchain_pb2_grpc.BlockChainStub(channel)
                    response = stub.AddBlock(blockchain_pb2.AddBlockRequest(data=data))
                    print("Client received block address: {}".format(response.hash))
        
        print(json.dumps(blockchain_dict, indent=2))
        print(BREAK_LINE)
        return blockchain_pb2.ProposeBlockResponse(node=node_name, hash=guess_hash)

# server setting
def serve():
    global node_network
    
    # command line argument: port, node name
    port = sys.argv[1]
    
    # remove local port
    node_network.remove(port)
    
    # run server
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    blockchain_pb2_grpc.add_BlockChainServicer_to_server(Blockchain(), server)
    server.add_insecure_port('127.0.0.1:' + port)
    server.start()
    print("Blockchain Node ({}) Started, Listening on port {}".format(node_name, port))
    server.wait_for_termination()

# run the server
if __name__ == '__main__':
    logging.basicConfig()
    serve()
