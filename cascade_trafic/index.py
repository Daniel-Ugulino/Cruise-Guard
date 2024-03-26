import cv2

# Load your custom cascade classifier
custom_cascade = cv2.CascadeClassifier("C:/Users/Daniel/Desktop/traffic_sign_recognition/cascade_trafic/cascade2/cascade.xml")

# Initialize the webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # Convert the frame to grayscale
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect objects using your custom cascade
    objects = custom_cascade.detectMultiScale(frame, minSize=(24, 24))
    
    # Draw rectangles around the detected objects
    for (x, y, w, h) in objects:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        face = frame[y:y+h, x:x+w]
        # Save the cropped face
        cv2.imwrite('detected_face.jpg', face)
        break
    
    # Display the resulting frame
    cv2.imshow('Object Detection', frame)
    
    # Check for 'q' key press to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()

# C:/Users/Daniel/Desktop/openCv/opencv/build/x64/vc15/bin/opencv_createsamples.exe -info pos.txt -w 42 -h 42 -num 500 -vec pos2.vec

# C:/Users/Daniel/Desktop/openCv/opencv/build/x64/vc15/bin/opencv_traincascade.exe -data cascade2/ -vec pos2.vec -bg neg.txt -precalcValBufSize 6000 -precalcIdxBufSize 6000 -numPos 500 -numNeg 700 -numStages 11 -w 32 -h 32 -maxFalseAlarmRate 0.2 -minHitRate 0.999