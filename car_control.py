import cv2
import numpy as np
from keras.models import load_model
import serial

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
    signal = "N"
    
    if(probabilidade >= 0.90):
        classe = indexVal
    
    if classe == 0:
        signal = "1" #20km
    elif classe == 2:
        signal = "2" #30km
    elif classe == 1:
        signal = "3" #70km
    elif classe == 3:
        signal = "4" #80km
    elif classe == 4:
        signal = "5" #120km
    elif classe == 5:
        signal = "P"  #Stop
    elif classe == 6:
        signal = "L" #Esquerda
    elif classe == 7:
        signal = "D" #Direita
    return signal

# model = load_model('./classification/modelo85_v5_best_best.h5')
# model = load_model('./classification/modelo30_v5.h5')
model = load_model('./classification/modelo85_v5_test.h5')

custom_cascade = cv2.CascadeClassifier("./cascade_trafic/cascade/cascade.xml")
cam = cv2.VideoCapture(0)
trafic_sign = []
last_signal = 'N'

esp = serial.Serial("COM5", 9600)
while True:
    ret, img = cam.read()
    img_A = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)   # Converter em Gray
    img_A = cv2.equalizeHist(img_A)   # Padronizar a Luminosidade das imagens
    objects = custom_cascade.detectMultiScale(img_A, minSize=(32, 32),minNeighbors=5,scaleFactor=1.03)
    trafic_sign = []
    for (x, y, w, h) in objects:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        trafic_sign = img[y:y+h, x:x+w]

    if(len(trafic_sign) > 1):
        signal = class_detector(trafic_sign)
        if(last_signal != signal and signal != "N"):
            last_signal = signal
            print(last_signal)
            esp.write((signal).encode())

    cv2.imshow('Object Detection', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cam.release()
        cv2.destroyAllWindows()
        break

cam.release()
cv2.destroyAllWindows()
