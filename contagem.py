import cv2 as cv #importando a biblioteca opencv e mudando o nome para cv
import numpy as np #importa a biblioteca da manipulação de dados numéricos e mudando seu nome para np 

video = cv.VideoCapture('videos/sorvete.mp4') #abrir o video selecionado

contador = 0 #contagem
sorvete_passando = False #inicia uma variável para a contagem

while video.isOpened(): #sempre que for verdadeiro igual um looping

    ret, img = video.read() #leitura do vídeo

    img = cv.resize(img, (1100,720),) #redimensiona para as dimensões desejadas

    imgGray = cv.cvtColor(img,cv.COLOR_RGB2GRAY) #deixa a imagem cinza
    x,y,w,h = 490,230,30,150 #define as coordenadas da área
    imgTh = cv.adaptiveThreshold(imgGray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 11, 12) #método Gaussiano que separa os objetos de interesse do fundo
    kernel = np.ones((8,8), np.uint8) #define um kernel para dilatação/expansão
    imgDil = cv.dilate(imgTh,kernel,iterations=2) #conecta áreas brancas próximas pela dilatação 

    recorte = imgDil[y:y+h,x:x+w] #recorta a região de interesse da imagem dilatada

    brancos = cv.countNonZero(recorte) #conta os pixels brancos na região de interesse

    if brancos > 400 and sorvete_passando == True: #verifica se a área tem um sorvete
        contador +=1 #acrescenta +1 na contagem se foi detectado um sorvete
    if brancos < 400: #verifica se a quantidade de pixels brancos na área de interesse é maior que 4000
        sorvete_passando = True #verifica se 'sorvete_passando' é verdadeiro
    else: #senão for
        sorvete_passando = False #verifica se 'sorvete_passando' é falso 

    if sorvete_passando == False: #se 'sorvete_passando' for igual a falso 
        cv.rectangle(img, (x, y), (x + 100, y + 100), (0, 255, 0), 4) #desenha um retângulo verde na imagem
    else:
        cv.rectangle(img,(x,y),(x+100,y+100),(255, 0, 255),4) #desenha um retângulo na imagem

    cv.rectangle(imgTh, (x, y), (x + w, y + h), (255, 255, 255), 6) #desenha um retângulo branco na imagem binarizada#

    cv.putText(img,str(brancos),(x-30,y-50),cv.FONT_HERSHEY_SIMPLEX,1,(255,255,255),1) #mostra a quantidade de pixels brancos na imagem
    cv.rectangle(img, (575,155), (575 + 88, 155 + 85), (255, 255, 255), -1) #desenha um retângulo branco para exibir o contador
    cv.putText(img, str(contador), (x+100, y), cv.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 5) #mostra o contador na imagem

    cv.imshow('video original', img) #mostra as anotações
    key = cv.waitKey(60) #espera 20 milissegundos (pode ser ajustado)

    if key == ord('q'):
        break


video.release()
cv.destroyAllWindows()
