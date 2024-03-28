import cv2

# Load your custom cascade classifier
custom_cascade = cv2.CascadeClassifier("./cascade/cascade.xml")

# Initialize the webcam
cap = cv2.VideoCapture(0)

def preprocessing(img):
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)   # Converter em Gray
    img = cv2.equalizeHist(img)   # Padronizar a Luminosidade das imagens
    return img

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    img = preprocessing(frame)
    
    # Detect objects using your custom cascade
    objects = custom_cascade.detectMultiScale(img, minSize=(32, 32),minNeighbors=5)
    
    # Draw rectangles around the detected objects
    for (x, y, w, h) in objects:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        face = frame[y:y+h, x:x+w]
        # Save the cropped face
        break
    
    # Display the resulting frame
    cv2.imshow('Object Detection', frame)
    
    # Check for 'q' key press to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()

# C:/Users/Daniel/Desktop/openCv/opencv/build/x64/vc15/bin/opencv_annotation.exe --annotations=pos.txt --images=./pos 

# C:/Users/Daniel/Desktop/openCv/opencv/build/x64/vc15/bin/opencv_createsamples.exe -info pos.txt -w 32 -h 32 -num 900 -vec pos.vec

# C:/Users/Daniel/Desktop/openCv/opencv/build/x64/vc15/bin/opencv_traincascade.exe -data cascade2/ -vec pos2.vec -bg neg.txt -precalcValBufSize 6000 -precalcIdxBufSize 6000 -numPos 565 -numNeg 2000 -numStages 11 -w 32 -h 32 -maxFalseAlarmRate 0.2 -minHitRate 0.999