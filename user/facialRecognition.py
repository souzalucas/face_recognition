import time
import grpc
import os
from concurrent import futures
import user_pb2, user_pb2_grpc

CHUNK_SIZE = 1 

# No init deverá ser passado o ip/porta do cliente para estabeler a comunicação
# e retornar o dado
class FacialRecognition:
    def __init__(self, address):
        channel = grpc.insecure_channel(address)
        self.stub = user_pb2_grpc.UserStub(channel)

        # Faz a criação do servidor
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        user_pb2_grpc.add_UserServicer_to_server(user_pb2_grpc.UserServicer, self.server)
        
    def save_chunks_to_file(self,chunks, filename):
        with open(filename, 'wb') as f:
            for chunk in chunks:
                f.write(chunk.buffer)

    # Functions Server
    def upload(self, request_iterator, context):
        save_chunks_to_file(request_iterator, self.tmp_file_name)
        return user_pb2.Reply(length=os.path.getsize(self.tmp_file_name))

    def startServer(self, port):
        self.server.add_insecure_port(f'[::]:{port}')
        # inicializa servidor
        self.server.start()

        try:
            while True:
                time.sleep(60 * 60 * 24)

        except KeyboardInterrupt:
            self.server.stop(0)

# Inicializa com endereço do cliente
Recognition = FacialRecognition(address='localhost:8001')

Recognition.startServer(8001)
