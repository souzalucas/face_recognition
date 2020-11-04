import os
from concurrent import futures

import grpc
import time

import trainingRecognition_pb2, trainingRecognition_pb2_grpc
import detection, recognition, training

CHUNK_SIZE = 1 # 1MB

# Funcao que divide o arquivo em partes
def get_file_chunks(filename):
  with open(filename, 'rb') as f:
    while True:
      piece = f.read(CHUNK_SIZE)
      if len(piece) == 0:
        return
      yield trainingRecognition_pb2.Piece(buffer=piece)

# Funcao que junta as partes do arquivo faz a gravacao
def save_chunks_to_file(chunks, filename):
  with open(filename, 'wb') as f:
    for chunk in chunks:
      f.write(chunk.buffer)

class ServerTrainingRecognition(trainingRecognition_pb2_grpc.TrainingRecognitionServicer):
  def __init__(self):

    class Servicer(trainingRecognition_pb2_grpc.TrainingRecognitionServicer):
      def __init__(self):
        # Instanciando detector e reconhecedor de faces
        self.detec = detection.DetectionFaces()
        # self.rec = recognition.RecognitionFaces()

      def saveImage(self, request_iterator, context):
        request_list = [request_rows for request_rows in request_iterator]

        # Captura informacoes do arquivo e do usuario
        file_name = request_list[0].fileName
        file_number = request_list[0].fileNumber
        user_name = request_list[0].userName

        # Criando pasta para o usuario, caso nao tenha
        if not os.path.isdir("server2_images/" + user_name):
          os.mkdir("server2_images/" + user_name)

        # Montando nome do arquivo
        tmp_file_name = "server2_images/" + user_name + "/" + file_name

        # Salva imagem em uma pasta para ser usada
        save_chunks_to_file(request_list, tmp_file_name)

        # Retorna status ao servidor 1
        message = "Imagem " + file_name + " Salva com sucesso"
        return trainingRecognition_pb2.ReplyRecognition(status = '0', message = message)

    self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    trainingRecognition_pb2_grpc.add_TrainingRecognitionServicer_to_server(Servicer(), self.server)

  def start(self, port):
    self.server.add_insecure_port(f'[::]:{port}')
    self.server.start()

    try:
      while True:
        time.sleep(60*60*24)
    except KeyboardInterrupt:
      self.server.stop(0)
