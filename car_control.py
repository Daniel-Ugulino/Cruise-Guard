import cv2
import numpy as np
from keras.models import load_model
import serial
import time

def check_connection(esp):
    try:
        esp.write(("T").encode())
        return True
    except serial.SerialTimeoutException:
        return False

def open_cam(port):
    print("Opening camera")
    try:
        cam = cv2.VideoCapture(port, cv2.CAP_FFMPEG)
        if not cam.isOpened():
            raise IOError(f"Failed to open camera at port {port}")
        return cam
    except Exception as e:
        print("Error:", e)
        return None
    
def load_models():
    print("Loading Models")
    try:
        classification_model = load_model('classification_model/traffic_sign_model.h5')
        object_detection_model = cv2.CascadeClassifier("./harcascade_model/cascade/cascade.xml")
        return classification_model, object_detection_model
    except Exception as e:
        print(e)
        return False, False
     
def esp_connection():
    print("Connecting to EPS32")
    try:
        esp = serial.Serial("COM5", 9600, timeout=20, write_timeout=15)
        print("Connected")
        return esp
    except serial.SerialException as e:
        print("Failed to establish connection:", e)
        return False

def preprocessing(img):
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)   # Converter em Gray
    img = cv2.equalizeHist(img)   # Padronizar a Luminosidade das imagens
    img = img / 255
    img_uint8 = np.uint8(img * 255)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    img = clahe.apply(img_uint8) / 255.0
    img = cv2.GaussianBlur(img, (3,3), 0)
    
    return img

def class_detector(img):
    # Dados da imagem
    model_class = -1
    img = cv2.resize(img,(64,64))
    img = preprocessing(img)
    img = img.reshape(1,64, 64, 1)
    result = classification_model.predict(img)
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
    cam = open_cam('http://192.168.29.81:80/')
    classification_model, object_detection_model = load_models()
    if(cam and classification_model and object_detection_model):
        while True:
            current_time = time.time()
            detected_sign = []
            
            ret, img = cam.read()
            objects = object_detection_model.detectMultiScale(img, minSize=(32, 32),minNeighbors=8)
            for (x, y, w, h) in objects:
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                detected_sign = img[y:y+h, x:x+w]

            if(len(detected_sign) > 1):
                detector = class_detector(detected_sign)
                signal = detector[0]
                if(last_signal != signal and signal != "N" or signal == "S"):
                    trafic_sign_text = detector[1]
                    last_signal = signal
                    if(esp):
                        if(esp.is_open):
                            esp.write((signal).encode())
                        else:
                            esp = False
                    else:
                        esp = False

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
                