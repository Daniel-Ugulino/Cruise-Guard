import cv2
import numpy as np
from keras.models import load_model
import os
import matplotlib.pyplot as plt

testPath = "./tests/"
model = load_model('./traffic_sign_model.h5')


def preprocessing(img):
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)   # Converter em Gray
    img = cv2.equalizeHist(img)   # Padronizar a Luminosidade das imagens
    img = img/255            # normalizar valores para 0 e 1 em vez de 0 e 255
    return img

def class_detector(img, img_name):
    # Dados da imagem
    classe = -1
    img = cv2.resize(img,(64,64))
    img = preprocessing(img)
    img = img.reshape(1,64, 64, 1)
    resultado = model.predict(img)
    indexVal = np.argmax(resultado)
    probabilidade = resultado[0, indexVal]

    if(probabilidade >= 0.90):
        classe = indexVal
    
    if classe == 0:
        placa = "20km"
    elif classe == 2:
        placa = "30km"
    elif classe == 1:
        placa = "70km"
    elif classe == 3:
        placa = "80km"
    elif classe == 4:
        placa = "120km"
    elif classe == 5:
        placa = "Stop"
    elif classe == 6:
        placa = "Esquerda"
    elif classe == 7:
        placa = "Direita"
    else:
        placa = "N"
    return ("placa:" + placa)

fig = plt.figure(figsize=(10, 7)) 
row = 1

for img in os.listdir(testPath):

    fig.add_subplot(3, 3, row) 
    Img = cv2.imread("./tests/"+img)
    text = class_detector(Img, img)
    plt.imshow(cv2.cvtColor(Img, cv2.COLOR_BGR2RGB))
    plt.title(text)
    plt.axis('off')
    row += 1

plt.show() 
