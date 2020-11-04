import grpc
import os
import time
from concurrent import futures
import recognitionFacial_pb2, recognitionFacial_pb2_grpc

CHUNK_SIZE = 1 # 1 MB

class FacialDetection:
    def __init__(self, address):
        # não utiliza ssl, sem credenciais
        # cria um canal com o ip:port
        channel = grpc.insecure_channel(address)
        self.stub = recognitionFacial_pb2_grpc.RecognitionFacialStub(channel)

        # Faz a criação do servidor
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        recognitionFacial_pb2_grpc.add_RecognitionFacialServicer_to_server(recognitionFacial_pb2_grpc.RecognitionFacialServicer, self.server)
        
    def get_file_chunks(self, filename):
      with open(filename, 'rb') as f:
          while True:
              piece = f.read(CHUNK_SIZE)
              if len(piece) == 0:
                  return
              yield recognitionFacial_pb2.Chunk(buffer=piece)

    def save_chunks_to_file(self, chunks, filename):
        with open(filename, 'wb') as f:
            for chunk in chunks:
                f.write(chunk.buffer)

    #---------------------------------------------------------------------------
    # Functions Client
    def uploadClient(self, in_file_name):
        chunks_generator = get_file_chunks(in_file_name)
        response = self.stub.upload(chunks_generator)
        assert response.length == os.path.getsize(in_file_name)

    # Functions Server
    def uploadServer(self, request_iterator, context):
        save_chunks_to_file(request_iterator, self.tmp_file_name)
        return recognitionFacial_pb2.Reply(length=os.path.getsize(self.tmp_file_name))

    # Inicializando server
    def startServer(self, port):
        self.server.add_insecure_port(f'[::]:{port}')
        # inicializa servidor
        self.server.start()

        try:
            while True:
                time.sleep(60 * 60 * 24)

        except KeyboardInterrupt:
            self.server.stop(0)

DetectionServer = FacialDetection(address='localhost:8001') # faz a conecção com o addr do servidor de reconhecimento

DetectionServer.startServer(8000) # inicializa servidor na porta 8000
