# project face recognition
# face_recognition
Um algoritmo de detecção e reconhecimento facial em Python3 utilizando a biblioteca OpenCV e conceitos de sistemas distribuídos.

O protocolo de comunicação utilizado será o TCP, e para a detecção e reconhecimento facial será usada a biblioteca OpenCV com diferentes algoritmos de aprendizado: Eigenface, Fisherface e Lbph.

## Arquitetura e funcionamento do sistema

<p align="center">
  <img src="Arquitetura Sistema Distribuído.png"/>
</p>

1. O usuário faz o envio de uma mensagem de acordo com um número identificador que irá indicar a operação.

	Exemplo:
	
	1. Enviar imagens para base de dados do servidor de treinamento e reconhecimento facial, para que posteriormente seja realizado o treinamento do algoritmo de aprendizado.

	2. Enviar imagem para detecção e reconhecimento facial.

2.  O servidor de detecção facial é responsável por receber a requisição do cliente, fazer a detecção de faces e encaminhar para o servidor de treinamento e reconhecimento, que irá realizar a operação de acordo com o identificador.
   
	-  As imagens que tiveram rostos detectados serão encaminhadas para o servidor de treinamento e reconhecimento facial.
    
	- As imagens que não tiveram rostos detectados serão retornadas ao usuário.
    

3.  O servidor de treinamento e reconhecimento facial receberá apenas as imagens que possuem rostos.
    

	Realiza a operação de acordo com o identificador:

	1. O servidor armazena a imagem localmente e realiza o treinamento.

		-  Caso o armazenamento seja realizado corretamente, retorna que a operação foi realizada com sucesso.
    
		- Caso aconteça algum problema, retorna uma mensagem contendo o respectivo erro.
    

	2. Utiliza a foto recebida e o arquivo de treinamento para executar o algoritmo de reconhecimento facial.

		- Caso reconheça as faces, retorna a identificação dos indivíduos que constam na foto.
    
		- Caso não reconheça nenhuma face, retorna para o usuário que as pessoas não foram identificadas.
