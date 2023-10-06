from concurrent import futures
import logging
import hashlib

import grpc
import blockchain_pb2
import blockchain_pb2_grpc

# The dictionary used to store the block
blockchain_dict = {}
block_hash_tmp = ""

# We implement the function at server class
class Blockchain(blockchain_pb2_grpc.BlockChainServicer):

    def AddBlock(self, request, context):
        global blockchain_dict
        global block_hash_tmp
        # In order to make sure that each data have different hash code, we use data+previous_hash to generate new hash
        data = request.data + block_hash_tmp
        # hash code generation, used for block address
        hash_code = hashlib.sha1(data.encode("utf-8")).hexdigest()
        # store the data and address at blockchain
        blockchain_dict[hash_code] = data
        block_hash_tmp = hash_code
        print(blockchain_dict)
        return blockchain_pb2.AddBlockResponse(hash=hash_code)

    def QueryBlock(self, request, context):
        self_block = blockchain_pb2.Block(hash=block_hash_tmp, data=blockchain_dict[block_hash_tmp])
        return blockchain_pb2.QueryBlockResponse(block=self_block)

# server setting
def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    blockchain_pb2_grpc.add_BlockChainServicer_to_server(Blockchain(), server)
    server.add_insecure_port('127.0.0.1:' + port)
    server.start()
    print("blockchain-demo started, listening on " + port)
    server.wait_for_termination()

# run the server
if __name__ == '__main__':
    logging.basicConfig()
    serve()
