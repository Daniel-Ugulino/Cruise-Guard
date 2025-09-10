import numpy as np
import os
import cv2
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout, BatchNormalization
from keras.utils import to_categorical
from keras.src.legacy.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt

trainPath = "./train/"
trainDir = os.listdir(trainPath)

L_Img = []
L_Cls = [] 
OriginalImgs = []

# Definição do tamanho padrão das imagens
nL= 64
nC= 64

def preprocessing(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img = np.array(255 * (img / 255) ** 0.8, dtype='uint8')
            
    img = cv2.resize(img, (64, 64), interpolation=cv2.INTER_CUBIC)

    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    img = clahe.apply(img)

    img = cv2.GaussianBlur(img, (3,3), 0)

    kernel = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])
    sharpened = cv2.filter2D(img, -1, kernel)

    img = cv2.addWeighted(img, 1.0, sharpened, 1.5, 0)

    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 7)

    img = cv2.bitwise_not(img)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=1)  
    img = cv2.erode(img, kernel, iterations=1)  
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=2)
    img = cv2.bitwise_not(img)

    return img

print("lendo imagens")
for dir in (trainDir):
    dir_imgs = os.listdir(trainPath+ str(dir) )
    for img in (dir_imgs):
        Img = cv2.imread(trainPath + dir + "/" + img)
        OriginalImgs.append(Img) 
        Img = cv2.resize(Img,(nL,nC))
        Img = preprocessing(Img)
        L_Img.append(Img) 
        L_Cls.append(dir)
print("foi")

arrayImg = np.asarray(L_Img)
arrayClasses = np.asarray(L_Cls)
arrayImg = arrayImg.reshape(arrayImg.shape[0], arrayImg.shape[1], arrayImg.shape[2], 1)

X_train, X_test, y_train, y_test = train_test_split(arrayImg, arrayClasses, test_size=0.2,shuffle=True)
X_train, X_validation, y_train, y_validation = train_test_split(X_train, y_train, test_size=0.2,shuffle=True)

dataGen= ImageDataGenerator(width_shift_range=0.1,   
                            height_shift_range=0.1,
                            zoom_range=0.2,  
                            shear_range=0.1,  
                            rotation_range=10)  
dataGen.fit(X_train)
batches= dataGen.flow(X_train,y_train,batch_size=200)

y_train = to_categorical(y_train, len(trainDir))
y_test = to_categorical(y_test,len(trainDir))
y_validation = to_categorical(y_validation,len(trainDir))

RNC = Sequential()
# 1a camada de convolução 
Cmd_C1= Conv2D(32,        # número de detectores de características
        kernel_size= (5,5), # ordem dos kernels dos detectores
        strides= (1,1),      # deslocamento da janela
        input_shape= [nL,nC,1], # shape da figura
        activation= 'relu')

RNC.add(Cmd_C1)
RNC.add(BatchNormalization())
Cmd_MP1= MaxPooling2D(pool_size= (2,2))
RNC.add(Cmd_MP1)

# 2a camada de convolução
Cmd_C2= Conv2D(64,kernel_size= (5,5), strides= (1,1),activation= 'relu')
RNC.add(Cmd_C2)
RNC.add(BatchNormalization())
Cmd_MP2= MaxPooling2D(pool_size= (2,2))
RNC.add(Cmd_MP2)

# 3a camada de convolução
Cmd_C3= Conv2D(64,kernel_size= (3,3),strides= (1,1),activation= 'relu')
RNC.add(Cmd_C3)
RNC.add(BatchNormalization())
Cmd_MP3= MaxPooling2D(pool_size= (2,2))
RNC.add(Cmd_MP3)

# 4a camada de convolução
Cmd_C4= Conv2D(32,kernel_size= (3,3),strides= (1,1),activation= 'relu')
RNC.add(Cmd_C4)
RNC.add(BatchNormalization())
Cmd_MP4 = MaxPooling2D(pool_size= (2,2))
RNC.add(Cmd_MP4)

# Flattening - Camada de entrada
RNC.add(Flatten())

# 1a Camada oculta 
RNC.add(Dense(units= 32,activation= 'relu'))
RNC.add(Dropout(0.5))

# Camada de saída
RNC.add(Dense(units= 8, activation= 'softmax')) # 1 classe

# Compilar rede
RNC.compile(loss='categorical_crossentropy',optimizer= 'adam',metrics= ['accuracy'])

# Treinamento da rede
print(RNC.summary())
history = RNC.fit(dataGen.flow(X_train,y_train, batch_size=200),epochs=80,validation_data=(X_validation,y_validation),shuffle=1)

score = RNC.evaluate(X_test,y_test,verbose=0)
print('Test Score:',score[0])
print('Test Accuracy:',score[1])

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.legend(['training', 'validation'])
plt.title('Loss')
plt.xlabel('Epoch')

RNC.save('traffic_sign_model_test_09.h5')
print('Modelo Salvo!')

plt.ioff()
plt.show()