import cv2
import os
import numpy as np

class Training():
  # def __init__(self):
  #   # Algoritmos
  #   self.eigenface = cv2.face.EigenFaceRecognizer_create()
  #   self.fisherface = cv2.face.FisherFaceRecognizer_create()
  #   self.lbph = cv2.face.LBPHFaceRecognizer_create()

  # Retorna as imagens dos rostos com seus respectivos ids (labels)
  # para serem usados no treinamento do algoritmo
  def getImageWithId(self, file_name):
    
    # Listas de faces e ids (labels)
    faces = []
    ids = []

    # Listando pastas dos individuos
    for root, dirnames, filenames in os.walk("./server2_images"):
      folders = dirnames
      break

    # Itera pelas pastas de cada individuo
    for idx,f in enumerate(folders, 1):

      # Capturando os caminhos das fotos daquele individuo
      paths = [os.path.join("./server2_images/"+f, a) for a in os.listdir("./server2_images/"+f)]

      # Itera sobre cada foto daquele individuo
      for imagePath in paths:
        # Converte imagem do rosto para tons de cinza
        imageFace = cv2.cvtColor(cv2.imread(imagePath), cv2.COLOR_BGR2GRAY)
        
        # Adiciona o id e a imagem do rosto em suas respectivas listas
        ids.append(idx)
        faces.append(imageFace)
      
      # Salvando arquivo de mapeamento 
      name_map = "./server2_images/map." + file_name.split(".")[0] + file_name.split(".")[1]  + ".txt"
      fileMap = open(name_map, 'a')
      fileMap.write(str(idx)+"="+f+"\n")
      fileMap.close()

    # Retorna as listas para treinamento
    return np.array(ids), faces, name_map

  # Realiza o treinamento do algoritmo Eigenface
  def eigenface(self, file_name):
    eigenFace = cv2.face.EigenFaceRecognizer_create()
    # Gerando labes para as imagens
    ids, faces, name_map = self.getImageWithId(file_name)

    # Treinando o algoritmo
    eigenFace.train(faces, ids)
 
    # Salvando arquivo de treinamento
    file_name = "./server2_images/classifierEigen." + file_name.split(".")[0] + file_name.split(".")[1] + ".yml"
    eigenFace.write(file_name)

    # Retorna o nome do arquivo de treinamento e mapeamento
    return file_name, name_map

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

