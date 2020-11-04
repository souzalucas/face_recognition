import time
import grpc
import os
from concurrent import futures
import recognitionFacial_pb2, recognitionFacial_pb2_grpc

# No init deverá ser passado o ip/porta do cliente para estabeler a comunicação
# e retornar o dado
CHUNK_SIZE = 1024 * 1024  # 1 MB

# def get_file_chunks(filename):
#   with open(filename, 'rb') as f:
#     while True:
#       piece = f.read(CHUNK_SIZE)
#       if len(piece) == 0:
#         return
#       yield recognitionFacial_pb2.Chunk(buffer=piece, nameFile=filename, identifier=str(1))


def save_chunks_to_file(chunks, filename):
  with open(filename, 'wb') as f:
    for chunk in chunks:
      f.write(chunk.buffer)

class RecognitionDetection(recognitionFacial_pb2_grpc.recognitionFacialServicer):
  def __init__(self):

    class Servicer(recognitionFacial_pb2_grpc.recognitionFacialServicer):
      def __init__(self):
        self.tmp_file_name = 'server_tmp'

      def uploadDetection(self, request_iterator, context):

        request_list = [request_rows for request_rows in request_iterator]

        print(request_list[0].nameFile)
      
        save_chunks_to_file(request_list, self.tmp_file_name)

        return recognitionFacial_pb2.Reply(length=os.path.getsize(self.tmp_file_name))

    self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    recognitionFacial_pb2_grpc.add_facialDetectionServicer_to_server(Servicer(), self.server)

  def start(self, port):
    self.server.add_insecure_port(f'[::]:{port}')
    self.server.start()

    try:
      while True:
        time.sleep(60*60*24)
    except KeyboardInterrupt:
      self.server.stop(0)

# DetectionServer = FacialDetection('localhost:8001') # faz a conecção com o addr do servidor de reconhecimento
FacialDetection = FacialDetection()
FacialDetection.start(8001) # inicializa servidor na porta 8000
# necessita do sevidor de reconhecimento em execução
# FacialDetection.server('localhost:8001')
