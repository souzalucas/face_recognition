from tkinter import *
from tkinter import scrolledtext
import tkinter.filedialog
from multiprocessing.pool import ThreadPool
import client
import cv2

class Application:
    def __init__(self, master=None, client=None):      

        # Cliente
        self.client = client

        # vetor do caminho das imagens selecionadas
        self.save_vet_images = []

        # Nome do algoritmo selecionado pelo usuario
        self.algoritmo = IntVar()

        # Coluna para enviar imagens
        self.frameEsquerdo = Frame(master, width = 300, height = 100, relief = 'raised')
        self.frameEsquerdo.grid(row = 1, column = 0,  sticky="nsew")

        # Coluna para reconhecer uma pessoa
        self.frameDireito = Frame(master, width = 300, height = 100, relief = 'raised')
        self.frameDireito.grid(row = 1, column = 1,  sticky="nsew")

        # Fonte do texto
        self.fontePadrao = ("Arial", "10")

        # Lado esquerdo
        self.primeiroContainer = Frame(self.frameEsquerdo)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.pack()

        #### Definicao dos containters da primeira coluna
        self.segundoContainer = Frame(self.frameEsquerdo)
        self.segundoContainer["padx"] = 20
        self.segundoContainer.pack()

        self.terceiroContainer = Frame(self.frameEsquerdo)
        self.terceiroContainer["padx"] = 20
        self.terceiroContainer["pady"] = 10
        self.terceiroContainer.pack()

        self.quartoContainer = Frame(self.frameEsquerdo)
        self.quartoContainer["pady"] = 10
        self.quartoContainer.pack()

        self.quintoContainer = Frame(self.frameEsquerdo)
        self.quintoContainer["pady"] = 10
        self.quintoContainer.pack()

        #### Botoes, labels, e caixas de texto da primeira coluna
        self.save_titulo = Label(self.primeiroContainer, text="Enviar suas fotos")
        self.save_titulo["font"] = ("Arial", "10", "bold")
        self.save_titulo.pack()

        self.save_nomeLabel = Label(self.segundoContainer,text="Nome", font=self.fontePadrao)
        self.save_nomeLabel.pack(side=LEFT)

        self.nome = Entry(self.segundoContainer)
        self.nome["width"] = 20
        self.nome["font"] = self.fontePadrao
        self.nome.pack(side=LEFT)

        self.save_botao_selecionar = Button(self.terceiroContainer)
        self.save_botao_selecionar["text"] = "Selecionar imagens"
        self.save_botao_selecionar["font"] = ("Calibri", "8")
        self.save_botao_selecionar["width"] = 15
        self.save_botao_selecionar["command"] = self.selecionar_imagens
        self.save_botao_selecionar.pack()

        self.save_botao_enviar = Button(self.terceiroContainer)
        self.save_botao_enviar["text"] = "Enviar imagens"
        self.save_botao_enviar["font"] = ("Calibri", "8")
        self.save_botao_enviar["width"] = 15
        self.save_botao_enviar["command"] = self.enviar_imagens
        self.save_botao_enviar.pack()

        self.save_mensagem = scrolledtext.ScrolledText(self.quartoContainer,width=20,height=5, )
        self.save_mensagem.pack()

        #### Definicao dos containters da segunda coluna
        self.quintoContainer = Frame(self.frameDireito)
        self.quintoContainer["pady"] = 10
        self.quintoContainer.pack()

        self.sextoContainer = Frame(self.frameDireito)
        self.sextoContainer["padx"] = 20
        self.sextoContainer.pack()

        self.setimoContainer = Frame(self.frameDireito)
        self.setimoContainer["pady"] = 10
        self.setimoContainer.pack()

        self.oitavoContainer = Frame(self.frameDireito)
        self.oitavoContainer["padx"] = 20
        self.oitavoContainer.pack()

        self.nonoContainer = Frame(self.frameDireito)
        self.nonoContainer["pady"] = 10
        self.nonoContainer.pack()

        self.decimoContainer = Frame(self.frameDireito)
        self.decimoContainer["pady"] = 10
        self.decimoContainer.pack()

        #### Botoes, labels, radios e caixas de texto da segunda coluna        
        self.rec_titulo = Label(self.quintoContainer, text="Reconhecer uma pessoa")
        self.rec_titulo["font"] = ("Arial", "10", "bold")
        self.rec_titulo.pack()

        self.rec_botao_selecionar = Button(self.sextoContainer)
        self.rec_botao_selecionar["text"] = "Selecionar imagem"
        self.rec_botao_selecionar["font"] = ("Calibri", "8")
        self.rec_botao_selecionar["width"] = 20
        self.rec_botao_selecionar["command"] = self.selecionar_imagens
        self.rec_botao_selecionar.pack()

        self.rec_algoritmo = Label(self.setimoContainer, text="Selecione o algoritmo")
        self.rec_algoritmo["font"] = ("Arial", "8", "bold")
        self.rec_algoritmo.pack()

        R1 = Radiobutton(self.oitavoContainer, text="Eigenface", variable=self.algoritmo, value=1)
        R1.pack( anchor = W )

        R2 = Radiobutton(self.oitavoContainer, text="Fisherface", variable=self.algoritmo, value=2)
        R2.pack( anchor = W )

        R3 = Radiobutton(self.oitavoContainer, text="LBPH", variable=self.algoritmo, value=3)
        R3.pack( anchor = W )

        self.rec_botao_eigen = Button(self.decimoContainer)
        self.rec_botao_eigen["text"] = "Reconhecer"
        self.rec_botao_eigen["font"] = ("Calibri", "8")
        self.rec_botao_eigen["width"] = 15
        self.rec_botao_eigen["command"] = self.reconhecer
        self.rec_botao_eigen.pack()

        self.rec_mensagem = scrolledtext.ScrolledText(self.nonoContainer,width=20,height=5)
        self.rec_mensagem.pack()

    # Funcao que usa uma interface grafica para o cliente selecionar as imagens
    def selecionar_imagens(self):
        window = tkinter.Tk()
        files = tkinter.filedialog.askopenfilenames(parent=window,title='Escolha as suas fotos')
        in_file_name = window.tk.splitlist(files)

        window.destroy()

        self.vet_images = in_file_name

    # Funcao que 
    def enviar_imagens(self):

        nome = self.nome.get()

        # Verifica se o nome foi escrito
        if (nome == ""):
            self.save_mensagem.insert(INSERT, "Escreva seu nome completo\n")
            return

        # Numero maximo de imagens
        pool = ThreadPool(processes=25)

        # Verifica a quantidade de imagens
        if (len(self.vet_images) == 0):
            self.save_mensagem.insert(INSERT, "Escolha pelo menos uma imagem para treinar\n")
            return

        # Executa as threads pra enviar as imagens
        arrayThreads = []
        for imagem in self.vet_images:
            # Chama a funcao do cliente que envia as fotos para armazenamento
            async_call = pool.apply_async(self.client.uploadImage, (imagem, str(self.nome.get())))
            
            arrayThreads.append(async_call)

        # Mostra as respostas dos envios na caixa de texto
        for threadx in arrayThreads:
            self.save_mensagem.insert(INSERT, threadx.get()+"\n")

    def reconhecer(self):

        # Verifica a quantidade de imagens
        if (len(self.vet_images) != 1):
            self.rec_mensagem.insert(INSERT, "Escolha UMA imagem para reconhecer\n")
            return

        # Verifica qual eh o algoritmo selecionado e executa-o
        if (self.algoritmo.get() == 1):
            # Chama a funcao do cliente que envia a foto para o reconhecimento
            resposta = self.client.recognition(self.vet_images[0], "eigenface")

            # Mostra a resposta na caixa de texto
            self.rec_mensagem.insert(INSERT, resposta + "\n")

        elif (self.algoritmo.get() == 2):
            resposta = self.client.recognition(self.vet_images[0], "fisherface")
            self.rec_mensagem.insert(INSERT, resposta + "\n")

        elif (self.algoritmo.get() == 3):
            resposta = self.client.recognition(self.vet_images[0], "lbph")
            self.rec_mensagem.insert(INSERT, resposta + "\n")

        else:
            self.rec_mensagem.insert(INSERT, "Escolha um algoritmo\n")
            return

if __name__ == '__main__':
    client = client.Client('localhost:8000')

    master = Tk()
    Application(master, client)
    master.mainloop()