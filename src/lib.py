import os
from concurrent import futures
import grpc
import time

from random import randint

import recognitionFacial_pb2, recognitionFacial_pb2_grpc

CHUNK_SIZE = 1  # 1MB

def get_file_chunks(filename):
    with open(filename, 'rb') as f:
        while True:
            piece = f.read(CHUNK_SIZE)
            if len(piece) == 0:
                return
            yield recognitionFacial_pb2.Chunk(buffer=piece)

def save_chunks_to_file(chunks, filename):
    with open(filename, 'wb') as f:
        for chunk in chunks:
            f.write(chunk.buffer)

class FileClient:
    def __init__(self, address):
        channel = grpc.insecure_channel(address)
        self.stub = recognitionFacial_pb2_grpc.recognitionFacialStub(channel)

    def upload(self, in_file_name):
        chunks_generator = get_file_chunks(in_file_name)
        response = self.stub.upload(chunks_generator)
        assert response.length == os.path.getsize(in_file_name)

class FileServer(recognitionFacial_pb2_grpc.recognitionFacialServicer):
    def __init__(self):

        class Servicer(recognitionFacial_pb2_grpc.recognitionFacialServicer):
            def __init__(self):
                self.tmp_file_name = '/tmp/server_tmp'
    
            def upload(self, request_iterator, context):
                save_chunks_to_file(request_iterator, self.tmp_file_name)
                return recognitionFacial_pb2.Reply(length=os.path.getsize(self.tmp_file_name))

        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        recognitionFacial_pb2_grpc.add_recognitionFacialServicer_to_server(Servicer(), self.server)

    def start(self, port):
        self.server.add_insecure_port(f'[::]:{port}')
        self.server.start()

        try:
            while True:
                time.sleep(60*60*24)
        except KeyboardInterrupt:
            self.server.stop(0)
