import os
from tkinter import Tk
import tkinter.filedialog
from tkinter import *
import grpc
import facialDetection_pb2, facialDetection_pb2_grpc

CHUNK_SIZE = 1024 * 1024   # 1MB

class User:
    def __init__(self, address):
        channel = grpc.insecure_channel(address)
        self.stub = facialDetection_pb2_grpc.facialDetectionStub(channel)
        

    def get_file_chunks(self, filename):
      with open(filename, 'rb') as f:
          while True:
              piece = f.read(CHUNK_SIZE)
              if len(piece) == 0:
                  return
              yield facialDetection_pb2.Chunk(buffer=piece,nameFile="teste.py",identifier="alanzito",ipPort="localhost:8000" ,op=1)


    def uploadClient(self, in_file_name):
        chunks_generator = self.get_file_chunks(in_file_name)
        response = self.stub.uploadDetection(chunks_generator)

        print(response)
        # assert response.length == os.path.getsize(in_file_name)

user = User('localhost:8000')

# root = tkinter.Tk()
# files = tkinter.filedialog.askopenfilenames(parent=root,title='Choose a file')
# in_file_name = root.tk.splitlist(files)

# print(in_file_name[0])

user.uploadClient('/media/alan/secundaria/face_recognition/PULSEIRA.png')
