import cv2

class DetectionFaces:
  def __init__(self):
    # Detector de faces
    self.detector = cv2.CascadeClassifier('opencv_cascades/haarcascade_frontalface_default.xml')

    # Permite que o openCV execute as funções de forma otimizada
    cv2.useOptimized()
    
  def start(self, image):
    # Converte para tons de cinza
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Faz a deteccao de faces
    detectedFaces = self.detector.detectMultiScale(grayImage, minNeighbors=9)
 
    # Retorna o numero de faces e o vetor de deteccao
    # e a imagem em cinza
    return len(detectedFaces), detectedFaces, grayImage
