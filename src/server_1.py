import os
from concurrent import futures
import grpc
import time
import cv2
from datetime import datetime

from proto import detection_pb2, detection_pb2_grpc
from proto import trainingRecognition_pb2, trainingRecognition_pb2_grpc

import opencvDetection, opencvRecognition, opencvTraining

CHUNK_SIZE = 1024 * 1024  # 1MB

# Funcao que divide o arquivo em partes e retorna a estrutura da requisicao
def get_file_chunks(file_name=None, user_name=None, classifier=None, op_id=None):
  with open(file_name, 'rb') as f:
    while True:
      piece = f.read(CHUNK_SIZE)
      if len(piece) == 0:
        return
      if(op_id == 1):
        yield trainingRecognition_pb2.Piece(buffer=piece, fileName = file_name.split("/")[1], 
                                            userName = user_name)
      else:
        yield trainingRecognition_pb2.Piece(buffer=piece, fileName = file_name.split("/")[1], 
                                            classifier=classifier)

# Funcao que junta as partes do arquivo faz a gravacao
def save_chunks_to_file(chunks, filename):
  with open(filename, 'wb') as f:
    for chunk in chunks:
      f.write(chunk.buffer)

class ServerDetection(detection_pb2_grpc.DetectionServicer):
  def __init__(self):

    class Servicer(detection_pb2_grpc.DetectionServicer):
      def __init__(self):
        # Instanciando a biblioteca implementada para
        # deteccao de faces
        self.opencvDetec = opencvDetection.DetectionFaces()

        # Conectando ao segundo servidor
        self.channel = grpc.insecure_channel('localhost:8001')
        self.stub = trainingRecognition_pb2_grpc.TrainingRecognitionStub(self.channel)

        # Permite que o openCV execute as funções de forma otimizada
        cv2.useOptimized()

      def imageSave(self, request_iterator, context):

        # Transforma o request_iterator em uma lista
        # para mais facil manipulacao
        request_list = [request_rows for request_rows in request_iterator]

        # Captura informacoes do arquivo e do usuario
        file_name = request_list[0].fileName
        user_name = request_list[0].userName

        # Criando pasta para o usuario, caso nao tenha
        if not os.path.isdir("server1_images"):
          os.mkdir("server1_images")

        # Montando nome do arquivo
        # A data e hora atual sao usadas no nome do arquivo
        # para evitar o conflito de nomes
        now = str(datetime.now()).split(".")[-1]
        tmp_file_name = "server1_images/" + user_name + "." + now + "." + file_name.split('.')[-1]

        # Salva imagem em uma pasta para ser usada
        save_chunks_to_file(request_list, tmp_file_name)

        # captura imagem salva para detectar as faces
        image = cv2.imread(tmp_file_name)

        # Chama a funcao para detectar as faces na imagem
        number_faces, detectedFaces, grayImage = self.opencvDetec.start(image)

        # A imagem deve conter apenas um rosto
        if(number_faces == 0):
          # Apaga imagem temporaria
          os.remove(tmp_file_name)
          return detection_pb2.ReplyDetection(status = '1', message = "Imagem " + file_name + " Não contém um rosto")
        elif(number_faces > 1):
          # Apaga imagem temporaria
          os.remove(tmp_file_name)
          return detection_pb2.ReplyDetection(status = '2', message = "Imagem " + file_name + " Tem mais de um rosto")
        else:
          # Corta a imagem pegando apenas o rosto
          for(x, y, l, a) in detectedFaces:
            imagemFace = cv2.resize(grayImage[y:y + a, x:x + l], (220, 220))
            cv2.imwrite(tmp_file_name, imagemFace)

          # Envia imagem para o servidor 2
          chunks_generator = get_file_chunks(file_name=tmp_file_name, user_name=user_name, op_id=1)
          response = self.stub.saveImage(chunks_generator)
          # Apaga imagem temporaria
          os.remove(tmp_file_name)
          # Retorna resposta do servidor 2
          return detection_pb2.ReplyDetection(status = response.status, message = response.message)

      def recognition(self, request_iterator, context):

        request_list = [request_rows for request_rows in request_iterator]

        # Captura informacoes do arquivo e do classificador a ser usado
        file_name = request_list[0].fileName
        classifier = request_list[0].classifier

        # Criando pasta para o usuario, caso nao tenha
        if not os.path.isdir("server1_images"):
          os.mkdir("server1_images")

        # Montando nome do arquivo
        # A data e hora atual sao usadas no nome do arquivo
        # para evitar o conflito de nomes
        now = datetime.now()
        tmp_file_name = "server1_images/" + str(now) + "." + file_name.split(".")[-1]

        # Salva imagem em uma pasta para ser usada
        save_chunks_to_file(request_list, tmp_file_name)

        # captura imagem salva para detectar as faces
        image = cv2.imread(tmp_file_name)

        # Chama a funcao para detectar as faces na imagem
        number_faces, detectedFaces, grayImage = self.opencvDetec.start(image)

        # A imagem deve conter apenas um rosto
        if(number_faces == 0):
          # Apaga imagem temporaria
          os.remove(tmp_file_name)
          return detection_pb2.ReplyDetection(status = '1', message = "Imagem não contém um rosto")
        elif(number_faces > 1):
          # Apaga imagem temporaria
          os.remove(tmp_file_name)
          return detection_pb2.ReplyDetection(status = '2', message = "Imagem tem mais de um rosto")
        else:
          # Envia imagem para o servidor 2
          chunks_generator = get_file_chunks(file_name=tmp_file_name, classifier=classifier, op_id=2)
          response = self.stub.recognize(chunks_generator)
          # Apaga imagem temporaria
          os.remove(tmp_file_name)
          # Retorna a resposta do servidor 2
          return detection_pb2.ReplyDetection(status = response.status, message = response.message)


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

if __name__ == '__main__':
  server = ServerDetection().start(8000)