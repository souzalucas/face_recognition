import os
from concurrent import futures

import grpc
import time

import detection_pb2, detection_pb2_grpc
import trainingRecognition_pb2, trainingRecognition_pb2_grpc
import detection, recognition, training

import cv2

from datetime import datetime


CHUNK_SIZE = 1  # 1MB

# Funcao que divide o arquivo em partes
def get_file_chunks(file_name, file_number, user_name):
  with open(file_name, 'rb') as f:
    while True:
      piece = f.read(CHUNK_SIZE)
      if len(piece) == 0:
        return
      yield trainingRecognition_pb2.Piece(buffer=piece, fileName = file_name.split("/")[1], 
                                           fileNumber = file_number, userName = user_name)

# Funcao que junta as partes do arquivo faz a gravacao
def save_chunks_to_file(chunks, filename):
  with open(filename, 'wb') as f:
    for chunk in chunks:
      f.write(chunk.buffer)

class ServerDetection(detection_pb2_grpc.DetectionServicer):
  def __init__(self):

    class Servicer(detection_pb2_grpc.DetectionServicer):
      def __init__(self):
        # Instanciando detector de faces
        self.detec = detection.DetectionFaces()

        # Conectando ao segundo servidor
        self.channel = grpc.insecure_channel('localhost:8889')
        self.stub = trainingRecognition_pb2_grpc.TrainingRecognitionStub(self.channel)

      def imageSave(self, request_iterator, context):

        request_list = [request_rows for request_rows in request_iterator]

        # Captura informacoes do arquivo e do usuario
        file_name = request_list[0].fileName
        file_number = request_list[0].fileNumber
        user_name = request_list[0].userName

        # Montando nome do arquivo
        tmp_file_name = "server1_images/" + user_name + "." + str(file_number) + "." + file_name.split('.')[-1]

        # Salva imagem em uma pasta para ser usada
        save_chunks_to_file(request_list, tmp_file_name)

        # captura imagem salva para detectar as faces
        image = cv2.imread(tmp_file_name)

        # Chama a funcao para detectar as faces na imagem
        number_faces, detectedFaces, grayImage = self.detec.start(image)

        if(number_faces == 0):
          return detection_pb2.ReplyImageSave(status = '1', message = "Imagem" + file_name + "Não contém um rosto")
        elif(number_faces > 1):
          return detection_pb2.ReplyImageSave(status = '2', message = "Imagem" + file_name + "Tem mais de um rosto")
        else:
          # Envia imagem para o servidor 2
          chunks_generator = get_file_chunks(tmp_file_name, file_number, user_name)
          response = self.stub.saveImage(chunks_generator)
          # Apaga imagem temporaria
          os.remove(tmp_file_name)
          # Retorna resposta do servidor 2
          return detection_pb2.ReplyImageSave(status = response.status, message = response.message)

      def recognition(self, request_iterator, context):

        request_list = [request_rows for request_rows in request_iterator]

        # Captura nome do arquivo
        file_name = request_list[0].fileName

        # Montando nome do arquivo
        now = datetime.now()
        tmp_file_name = "server1_images/" + str(now) + file_name.split(".")[-1]

        # Salva imagem em uma pasta para ser usada
        save_chunks_to_file(request_list, tmp_file_name)

        # captura imagem salva para detectar as faces
        image = cv2.imread(tmp_file_name)

        # Chama a funcao para detectar as faces na imagem
        number_faces, detectedFaces, grayImage = self.detec.start(image)

        # if (number_faces > 0)

        return detection_pb2.ReplyRecognition(status = '0', message = "Salvo")

    self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    detection_pb2_grpc.add_DetectionServicer_to_server(Servicer(), self.server)

  def start(self, port):
    self.server.add_insecure_port(f'[::]:{port}')
    self.server.start()

    try:
      while True:
        time.sleep(60*60*24)
    except KeyboardInterrupt:
      self.server.stop(0)
