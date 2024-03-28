import cv2
import numpy as np
from keras.models import load_model
import serial

model = load_model('./classification_model/traffic_sign_model.h5')
custom_cascade = cv2.CascadeClassifier("./harcascade_model/cascade/cascade.xml")
cam = cv2.VideoCapture(0)
last_signal = 'N'
placa = 'None'
# esp = serial.Serial("COM5", 9600)

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
    
    if(probabilidade >= 0.95):
        classe = indexVal

    match classe:
        case 0:
            return "1", "20km"
        case 1:
            return "3", "70km"
        case 2:
            return "2", "30km"
        case 3:
            return "4", "80km"
        case 4:
            return "5", "120km"
        case 5:
            return "P", "Stop"
        case 6:
            return "L", "Esquerda"
        case 7:
            return "D", "Direita"
        case _:
            return "N", "None" 

while True:
    trafic_sign = []
    ret, img = cam.read()
    objects = custom_cascade.detectMultiScale(img, minSize=(32, 32),minNeighbors=8,scaleFactor=1.1)
    for (x, y, w, h) in objects:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        trafic_sign = img[y:y+h, x:x+w]

    if(len(trafic_sign) > 1):
        detector = class_detector(trafic_sign)
        signal = detector[0]
        if(last_signal != signal and signal != "N"):
            placa = detector[1]
            last_signal = signal
            print(last_signal)
            # esp.write((signal).encode())

    img = cv2.putText(img, placa, (250, 100) , cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0) , 2, cv2.LINE_AA) 
    cv2.imshow('Object Detection', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cam.release()
        cv2.destroyAllWindows()
        break

cam.release()
cv2.destroyAllWindows()
