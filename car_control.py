import cv2
import numpy as np
from keras.models import load_model
import serial
import time


def open_cam(port):
    try:
        cam = cv2.VideoCapture(port)
        if not cam.isOpened():
            raise IOError(f"Failed to open camera at port {port}")
        return cam
    except Exception as e:
        print("Error:", e)
        return None
    
def load_models():
    try:
        model = load_model('classification_model/traffic_sign_model.h5')
        custom_cascade = cv2.CascadeClassifier("./harcascade_model/cascade/cascade.xml")
        return model, custom_cascade
    except Exception as e:
        print(e)
        return False, False
     
def esp_connection():
    try:
        print("Connecting to EPS32")
        esp = serial.Serial("COM5", 9600, timeout=20)
        print("Connected")
        return esp
    except serial.SerialException as e:
        print("Failed to establish connection:", e)
        return False

def preprocessing(img):
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)   # Converter em Gray
    img = cv2.equalizeHist(img)   # Padronizar a Luminosidade das imagens
    img = img/255            # normalizar valores para 0 e 1 em vez de 0 e 255
    return img

def class_detector(img):
    # Dados da imagem
    model_class = -1
    img = cv2.resize(img,(64,64))
    img = preprocessing(img)
    img = img.reshape(1,64, 64, 1)
    result = model.predict(img)
    indexVal = np.argmax(result)
    probability = result[0, indexVal]
    
    if(probability >= 0.95):
        model_class = indexVal

    match model_class:
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
            return "S", "Stop"
        case 6:
            return "L", "Left"
        case 7:
            return "R", "Right"
        case _:
            return "N", "None" 

if __name__ == "__main__":
    last_signal = 'N'
    trafic_sign_text = 'None'
    start_time = time.time()
    esp = esp_connection()
    cam = open_cam(0)
    model, custom_cascade = load_models()
    if(cam and model and custom_cascade):
        while True:
            current_time = time.time()
            detected_sign = []
            
            ret, img = cam.read()
            objects = custom_cascade.detectMultiScale(img, minSize=(32, 32),minNeighbors=8)
            for (x, y, w, h) in objects:
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                detected_sign = img[y:y+h, x:x+w]

            if(len(detected_sign) > 1):
                detector = class_detector(detected_sign)
                signal = detector[0]
                if(last_signal != signal and signal != "N" or signal == "P"):
                    trafic_sign_text = detector[1]
                    last_signal = signal
                    if(esp):
                        esp.write((signal).encode())

            img = cv2.putText(img, trafic_sign_text, (250, 100) , cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0) , 2, cv2.LINE_AA) 

            if(not esp and (current_time - start_time >= 30)):
                esp = esp_connection()
                start_time = time.time()

            cv2.imshow('Cruise Guard', img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cam.release()
                cv2.destroyAllWindows()
                if(esp):
                    esp.close()
                break
                