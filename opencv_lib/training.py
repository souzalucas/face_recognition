import cv2
import os
import numpy as np

class Training():
  def __init__(self):
    # Algoritmos
    self.eigenface = cv2.face.EigenFaceRecognizer_create()
    self.fisherface = cv2.face.FisherFaceRecognizer_create()
    self.lbph = cv2.face.LBPHFaceRecognizer_create()

  # Retorna as imagens dos rostos com seus respectivos ids (labels)
  # para serem usados no treinamento do algoritmo
  def getImageWithId(self):
    # Capturando todos os caminhos das fotos
    paths = [os.path.join('fotos', f) for f in os.listdir('fotos')]

    # Listas de faces e ids (labels)
    faces = []
    ids = []

    for imagePath in paths:
      # Converte imagem do rosto para tons de cinza
      imageFace = cv2.cvtColor(cv2.imread(imagePath), cv2.COLOR_BGR2GRAY)

      # Captura o id da imagem
      id = int(os.path.split(imagePath)[-1].split('.')[1])

      # Adiciona o id e a imagem do rosto em suas respectivas listas
      ids.append(id)
      faces.append(imageFace)

    # Retorna as listas para treinamento
    return np.array(ids), faces

  # Realiza o treinamento do algoritmo Eigenface
  def eigenface(self):
    # Gerando labes para as imagens
    ids, faces = self.getImageWithId()

    # Treinando o algoritmo
    eigenface.train(faces, ids)
 
    # Salvando arquivo de treinamento
    eigenface.write('classifierEingen.yml')

  # Realiza o treinamento do algoritmo Fisherface
  def fisherFace(self):
    # Gerando labes para as imagens
    ids, faces = self.getImageWithId()

    # Treinando o algoritmo
    fisherface.train(faces, ids)
 
    # Salvando arquivo de treinamento
    fisherface.write('classifierFisherface.yml')
    
  # Realiza o treinamento do algoritmo LBPH
  def lbph(self):
    # Gerando labes para as imagens
    ids, faces = self.getImageWithId()

    # Treinando o algoritmo
    lbph.train(faces, ids)
 
    # Salvando arquivo de treinamento
    lbph.write('classifierLbph.yml')

