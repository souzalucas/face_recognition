from concurrent import futures
import grpc
import time
from proto import detection_pb2, detection_pb2_grpc
from tkinter import Tk
import tkinter.filedialog
from tkinter import *
import threading
import gui

# Funcao que divide o arquivo em partes e retorna a estrutura da requisicao
def get_file_chunks(file_name=None, user_name=None, classifier=None, op_id=None):
  with open(file_name, 'rb') as f:
    while True:
      piece = f.read(1024*1024)
      if len(piece) == 0:
        return
      if(op_id == 1):
        yield detection_pb2.Chunk(buffer=piece, fileName = file_name, userName = user_name)
      else:
        yield detection_pb2.Chunk(buffer=piece, classifier=classifier, fileName = file_name)

class Client:
  def __init__(self, address):
    channel = grpc.insecure_channel(address)
    self.stub = detection_pb2_grpc.DetectionStub(channel)

  # Funcao que envia as imagens para o servidor armazenar
  def uploadImage(self, file_name, user_name):
    chunks_generator = get_file_chunks(file_name=file_name, user_name=user_name, op_id=1)
    response = self.stub.imageSave(chunks_generator)
    if (response.status == '0'):
      return "Imagem " + file_name + " armazenada!"
    elif (response.status == '1' or response.status == '2'):
      return response.message
  
  # Funcao que envia uma imagem para o servidor detectar um rosto
  def recognition(self, file_name, classifier):
    chunks_generator = get_file_chunks(file_name=file_name, classifier=classifier, op_id=2)
    response = self.stub.recognition(chunks_generator)
    if (response.status == '0'):
      return str(response.message) + " está na foto!"
    elif (response.status == '1' or response.status == '2' or response.status == '3'):
      return response.message

  