import cv2
import numpy as np
from keras.models import load_model
import os

testPath = "./tests/"
model = load_model('./modelo85_v5_best_best.h5')


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
        signal = "1"
    elif classe == 2:
        placa = "30km"
        signal = "2"
    elif classe == 1:
        placa = "70km"
        signal = "3"
    elif classe == 3:
        placa = "80km"
        signal = "4"
    elif classe == 4:
        placa = "120km"
        signal = "5"
    elif classe == 5:
        placa = "Stop"
        signal = "P"
    elif classe == 6:
        placa = "Esquerda"
        signal = "L"
    elif classe == 7:
        placa = "Direita"
        signal = "D"
    else:
        placa = "N"
        signal = "N"
    print(str(classe) + " placa:" + placa + " arquivo:" + str(img_name))
    return signal

for img in os.listdir(testPath):
    Img = cv2.imread("./tests/"+img)
    class_detector(Img, img)