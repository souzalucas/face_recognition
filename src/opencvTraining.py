import cv2
import os
import numpy as np

class Training():
  def __init__(self):
    # Algoritmos
    self.classifierEigenface = cv2.face.EigenFaceRecognizer_create()
    self.classifierFisherface = cv2.face.FisherFaceRecognizer_create()
    self.classifierLbph = cv2.face.LBPHFaceRecognizer_create()

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

  # Funcao para treinar o algoritmo de reconhecimento
  # O nome do algoritmo deve ser passado no parametro classifier_name
  def train(self, file_name, classifier_name):
    # Gerando labes para as imagens
    ids, faces, name_map = self.getImageWithId(file_name)

    # Treinando o algoritmo e gravando arquivo de treinamento
    if (classifier_name == "eigenface"):
      self.classifierEigenface.train(faces, ids)
      file_name = "./server2_images/classifierEigen." + file_name.split(".")[0] + file_name.split(".")[1] + ".yml"
      self.classifierEigenface.write(file_name)

    elif (classifier_name == "fisherface"):
      self.classifierFisherface.train(faces, ids)
      file_name = "./server2_images/classifierFisher." + file_name.split(".")[0] + file_name.split(".")[1] + ".yml"
      self.classifierFisherface.write(file_name)

    elif (classifier_name == "lbph"):
      self.classifierLbph.train(faces, ids)
      file_name = "./server2_images/classifierLbph." + file_name.split(".")[0] + file_name.split(".")[1] + ".yml"
      self.classifierLbph.write(file_name)
    
    # Retorna o nome do arquivo de treinamento e mapeamento
    return file_name, name_map

