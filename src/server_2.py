import os
from concurrent import futures
import grpc
import time
import cv2
from datetime import datetime


from proto import trainingRecognition_pb2, trainingRecognition_pb2_grpc

import opencvDetection, opencvRecognition, opencvTraining

CHUNK_SIZE = 1024 * 1024 # 1MB

# Funcao que junta as partes do arquivo faz a gravacao
def save_chunks_to_file(chunks, filename):
  with open(filename, 'wb') as f:
    for chunk in chunks:
      f.write(chunk.buffer)

class ServerTrainingRecognition(trainingRecognition_pb2_grpc.TrainingRecognitionServicer):
  def __init__(self):

    class Servicer(trainingRecognition_pb2_grpc.TrainingRecognitionServicer):
      def __init__(self):
        # Instanciando as bibliotecas implementadas para
        # deteccao, treinamento e o reconhecimento
        self.opencvDetec = opencvDetection.DetectionFaces()
        self.opencvTrain = opencvTraining.Training()
        self.opencvRec = opencvRecognition.RecognitionFaces()

        # Permite que o openCV execute as funções de forma otimizada
        cv2.useOptimized()

      def saveImage(self, request_iterator, context):
        request_list = [request_rows for request_rows in request_iterator]

        # Captura informacoes do arquivo e do usuario
        file_name = request_list[0].fileName
        user_name = request_list[0].userName

        # Criando pasta para o usuario, caso nao tenha
        if not os.path.isdir("server2_images"):
          os.mkdir("server2_images")

        # Criando pasta para o usuario, caso nao tenha
        if not os.path.isdir("server2_images/" + user_name):
          os.mkdir("server2_images/" + user_name)

        # Montando nome do arquivo
        now = str(datetime.now()).split(".")[-1]
        tmp_file_name = "server2_images/" + user_name + "/" + file_name

        # Salva imagem em uma pasta para ser usada
        save_chunks_to_file(request_list, tmp_file_name)

        # Retorna status ao servidor 1
        message = "Imagem salva com sucesso no servidor"
        return trainingRecognition_pb2.ReplyRecognition(status = '0', message = message)

      def recognize(self, request_iterator, context):
        
        # Transforma o request_iterator em uma lista
        # para mais facil manipulacao
        request_list = [request_rows for request_rows in request_iterator]

        # Captura informacoes do arquivo e do classificador a ser usado
        file_name = request_list[0].fileName
        classifier = request_list[0].classifier

        # Criando pasta para o usuario, caso nao tenha
        if not os.path.isdir("server2_images"):
          os.mkdir("server2_images")

        # Montando nome do arquivo
        tmp_file_name = "server2_images/img." + file_name

        # Salva imagem para ser usada
        save_chunks_to_file(request_list, tmp_file_name)

        # Realiza o treinamento do algoritmo
        yml_file_name, map_file_name = self.opencvTrain.train(file_name, classifier)

        # Faz o reconhecimento do individuo
        image = cv2.imread(tmp_file_name)
        person = self.opencvRec.recognition(image, map_file_name, yml_file_name, classifier)

        # Exclui os arquivos temporarios
        os.remove(tmp_file_name)
        os.remove(yml_file_name)
        os.remove(map_file_name)

        # Retorna o resultado
        if (person == "1"):
          return trainingRecognition_pb2.ReplyRecognition(status = '3', message = "Pessoa não reconhecida!")
        else:
          return trainingRecognition_pb2.ReplyRecognition(status = '0', message = person)

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

if __name__ == '__main__':
  server = ServerTrainingRecognition().start(8001)