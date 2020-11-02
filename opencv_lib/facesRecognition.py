import cv2
import numpy as np
import os
import facesDetection

class RecFaces:
  def __init__(self):
    # Detector de faces
    self.detector = facesDetection.DetecFaces()

    self.font = cv2.FONT_HERSHEY_COMPLEX_SMALL

    # Algoritmos
    self.eigenface = cv2.face.EigenFaceRecognizer_create()
    self.fisherface = cv2.face.FisherFaceRecognizer_create()
    self.lbph = cv2.face.LBPHFaceRecognizer_create()

  # Reconhecedor Eingenface
  def eigenFace(self, image):
    # Arquivo de treinamento
    self.eigenface.read('classificadorEingen.yml')

    # Faz a deteccao de faces
    number, detectedFaces, grayImage = self.detector.start(image)

    # Realiza o reconhecimento
    for(x, y, l, a) in detectedFaces:
      imageFace = cv2.resize(grayImage[y:y + a, x:x + l], (220, 220))
      cv2.rectangle(image, (x, y), (x + l, y + a), (0, 0, 255), 2)
      id, confidence = self.eigenface.predict(imageFace)
      cv2.putText(image, str(id), (x, y + (a + 30)), self.font, 2, (0,0,255))
      print(id)

  # def fisherFace(self, image):
  #   self.eigenFace.read('classifierEingen.yml')

  # def lbph(self, image):
  #   self.eigenFace.read('classifierEingen.yml')
