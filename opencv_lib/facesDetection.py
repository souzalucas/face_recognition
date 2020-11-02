import cv2
import numpy as np
import os

class DetecFaces:
  def __init__(self):
    # Detector de faces
    self.detector = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
    
  def start(self, image):
    # Transforma para tons de cinza
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Faz a deteccao de faces
    detectedFaces = self.detector.detectMultiScale(grayImage, minNeighbors=9)
 
    # Retorna o numero de faces e o vetor de deteccao
    # e a imagem em cinza
    return len(detectedFaces), detectedFaces, grayImage
