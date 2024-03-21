import cv2
import numpy as np
from keras.models import load_model
import serial

# cam_port = 1
# cam = cv2.VideoCapture(cam_port) 


def preprocessing(img):
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)   # Converter em Gray
    img = cv2.equalizeHist(img)   # Padronizar a Luminosidade das imagens
    img = img/255            # normalizar valores para 0 e 1 em vez de 0 e 255
    return img

def class_detector(img):
    # Dados da imagem
    classe = -1
    img = cv2.resize(img,(64,64))
    img = preprocessing(img)
    img = img.reshape(1,64, 64, 1)
    resultado = model.predict(img)
    indexVal = np.argmax(resultado)
    probabilidade = resultado[0, indexVal]

    if(probabilidade >= 0.80):
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
    print(placa)
    return signal

model = load_model('./classification/modelo85_v5_best_best.h5')
custom_cascade = cv2.CascadeClassifier("./cascade_trafic/cascade/cascade.xml")
cam = cv2.VideoCapture(0)
trafic_sign = []
last_signal = 'N'

# Mostrar a imagem
# esp = serial.Serial("COM5", 9600)
img = cv2.imread('C:/Users/Daniel/Desktop/projeto_PB/test_img.jpg')
while True:
    ret, img = cam.read()
    objects = custom_cascade.detectMultiScale(img, minSize=(24, 24))
    trafic_sign = []
    for (x, y, w, h) in objects:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        trafic_sign = img[y:y+h, x:x+w]

    if(len(trafic_sign) > 1):
        signal = class_detector(trafic_sign)
        if(last_signal != signal):
            last_signal = signal
            # esp.write((signal).encode())

    print(last_signal)
    cv2.imshow('Object Detection', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()


