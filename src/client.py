import os
from concurrent import futures

import grpc
import time
import sys
import detection_pb2, detection_pb2_grpc

CHUNK_SIZE = 1024 * 1024  # 1MB

def get_chunks_save(file_name, file_number, user_name):
  with open(file_name, 'rb') as f:
    while True:
      piece = f.read(CHUNK_SIZE)
      if len(piece) == 0:
        return
      yield detection_pb2.Chunk(buffer=piece, fileName = file_name, 
                                fileNumber = file_number, userName = user_name)
                                
def get_chunks_rec(file_name):
  with open(file_name, 'rb') as f:
    while True:
      piece = f.read(CHUNK_SIZE)
      if len(piece) == 0:
        return
      yield detection_pb2.Chunk(buffer=piece, fileName = file_name)

def save_chunks_to_file(chunks, filename):
  with open(filename, 'wb') as f:
    for chunk in chunks:
      f.write(chunk.buffer)

class Client:
  def __init__(self, address):
    channel = grpc.insecure_channel(address)
    self.stub = detection_pb2_grpc.DetectionStub(channel)

  def upload(self, file_name, file_number, user_name):
    chunks_generator = get_chunks_save(file_name, file_number, user_name)
    response = self.stub.imageSave(chunks_generator)
    print(response.message)
  
  def recognition(self, file_name):
    chunks_generator = get_chunks_rec(file_name)
    response = self.stub.recognition(chunks_generator)
    # print(response.message)

if __name__ == '__main__':
  client = Client('localhost:8888')

  # Enviando imagem pra salvar no servidor 2
  file_name = sys.argv[1]

  client.upload(file_name, int(file_name.split(".")[0]), 'Lucas')

  # Enviando imagem para reconhecer
  # client.recognition(file_name)
  