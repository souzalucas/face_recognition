import cv2
import numpy as np
import os
import detection

class RecognitionFaces:
  def __init__(self):
    # Detector de faces
    self.detector = detection.DetectionFaces()

    # Fonte para escrita do identificador
    # self.font = cv2.FONT_HERSHEY_COMPLEX_SMALL

    # Algoritmos
    # self.eigenface = cv2.face.EigenFaceRecognizer_create()
    # self.fisherface = cv2.face.FisherFaceRecognizer_create()
    # self.lbph = cv2.face.LBPHFaceRecognizer_create()

  # Reconhecedor Eingenface
  def eigenface(self, image, map_file_name, yml_file_name):
    eigenFace = cv2.face.EigenFaceRecognizer_create()

    # Arquivo do algoritmo treinado
    eigenFace.read(yml_file_name)

    # Faz a deteccao de faces
    number, detectedFaces, grayImage = self.detector.start(image)

    # Realiza o reconhecimento
    for(x, y, l, a) in detectedFaces:
      # Faz o corte da imagem deixando apenas o rosto
      imageFace = cv2.resize(grayImage[y:y + a, x:x + l], (220, 220))
      
      # Desenha o ratangulo em volta do rosto na imagem original
      # cv2.rectangle(image, (x, y), (x + l, y + a), (0, 0, 255), 2)
      
      # Reconhece o individuo retornando seu id e a confianca
      idx, confidence = eigenFace.predict(imageFace)

      # Procura o nome da pessoa no arquivo de mapeamento
      with open(map_file_name) as file_map:
        for line in file_map:
          if(int(line.split("=")[0]) == idx):
            # Retorna o nome do individuo
            return  (line.split("=")[-1]).rstrip('\n')
    
    return "1"

      # Escreve o id do individuo na imagem original
      # cv2.putText(image, str(id), (x, y + (a + 30)), self.font, 2, (0,0,255))

    # Retorna a imagem original com a identificacao dos individuos
    # return image

  # def fisherFace(self, image):
  #   self.eigenFace.read('classifierEingen.yml')

  # def lbph(self, image):
  #   self.eigenFace.read('classifierEingen.yml')
