from concurrent import futures
import grpc
import time
import detection_pb2, detection_pb2_grpc

CHUNK_SIZE = 1024 * 1024  # 1MB

# Funcao que divide o arquivo em partes
def get_file_chunks(file_name=None, user_name=None, op_id=None):
  with open(file_name, 'rb') as f:
    while True:
      piece = f.read(CHUNK_SIZE)
      if len(piece) == 0:
        return
      if(op_id == 1):
        yield detection_pb2.Chunk(buffer=piece, fileName = file_name, userName = user_name)
      else:
        yield detection_pb2.Chunk(buffer=piece, fileName = file_name)

class Client:
  def __init__(self, address):
    channel = grpc.insecure_channel(address)
    self.stub = detection_pb2_grpc.DetectionStub(channel)

  def uploadImage(self, file_name, user_name):
    chunks_generator = get_file_chunks(file_name, user_name, 1)
    response = self.stub.imageSave(chunks_generator)
    print(response.message)
  
  def recognition(self, file_name):
    chunks_generator = get_file_chunks(file_name=file_name, op_id=2)
    response = self.stub.recognition(chunks_generator)
    print(response.message)

if __name__ == '__main__':
  client = Client('localhost:8000')

  # Enviando imagem pra salvar no servidor 2
  # file_name = sys.argv[1]

  # client.uploadImage("4.jpg", 'Rodolfo')
  client.recognition('4.jpg')