import lib
import grpc
import os
import time
from ..facial_recognition_server import recognitionFacial_pb2, recognitionFacial_pb2_grpc

CHUNK_SIZE = 1 # 1 MB

class facialDetectionServer:
    def __init__(self, address):
        channel = grpc.insecure_channel(address)
        self.stub = recognitionFacial_pb2_grpc.recognitionFacialStub(channel)
        
    def get_file_chunks(self, filename):
      with open(filename, 'rb') as f:
          while True:
              piece = f.read(CHUNK_SIZE)
              if len(piece) == 0:
                  return
              yield recognitionFacial_pb2.Chunk(buffer=piece)

    def upload(self, in_file_name):
        chunks_generator = get_file_chunks(in_file_name)
        response = self.stub.upload(chunks_generator)
        assert response.length == os.path.getsize(in_file_name)
    
    def start(self, port):
        self.server.add_insecure_port(f'[::]:{port}')
        self.server.start()

        try:
            while True:
                time.sleep(60*60*24)
        except KeyboardInterrupt:
            self.server.stop(0)

facialDetectionServer().start(8000) # inicializa servidor na porta 8000

facialDetectionServer = facialDetectionServer('localhost:8001') # faz a conecção com o addr do servidor de reconhecimento