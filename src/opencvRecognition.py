import cv2
import opencvDetection

class RecognitionFaces:
  def __init__(self):
    # Instanciando a biblioteca implementada para
    # deteccao de faces
    self.opencvDetec = opencvDetection.DetectionFaces()

    # Algoritmos
    self.classifierEigenface = cv2.face.EigenFaceRecognizer_create()
    self.classifierFisherface = cv2.face.FisherFaceRecognizer_create()
    self.classifierLbph = cv2.face.LBPHFaceRecognizer_create()

    # Permite que o openCV execute as funções de forma otimizada
    cv2.useOptimized()

  # Funcao que faz o reconhecimento do individuo em uma foto
  # O nome do algoritmo deve ser passado no parametro classifier_name
  def recognition(self, image, map_file_name, yml_file_name, classifier_name):

    idx = 1

    # Faz a deteccao de faces
    number, detectedFaces, grayImage = self.opencvDetec.start(image)

    # Realiza o reconhecimento
    for(x, y, l, a) in detectedFaces:
      # Faz o corte da imagem deixando apenas o rosto
      imageFace = cv2.resize(grayImage[y:y + a, x:x + l], (220, 220))
           
      # Escolhe o algoritmo de reconhecimento
      if (classifier_name == "eigenface"):
        # Arquivo do algoritmo treinado
        self.classifierEigenface.read(yml_file_name)

        # Reconhece o individuo retornando seu id e a confianca
        idx, confidence = self.classifierEigenface.predict(imageFace)

      elif (classifier_name == "fisherface"):
        self.classifierFisherface.read(yml_file_name)

        idx, confidence = self.classifierFisherface.predict(imageFace)

      elif (classifier_name == "lbph"):
        self.classifierLbph.read(yml_file_name)

        idx, confidence = self.classifierLbph.predict(imageFace)

      # Procura o nome da pessoa no arquivo de mapeamento
      with open(map_file_name) as file_map:
        for line in file_map:
          if(int(line.split("=")[0]) == idx):
            # Retorna o nome do individuo
            return  (line.split("=")[-1]).rstrip('\n')
    
    return "1"
