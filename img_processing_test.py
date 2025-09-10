import cv2
import numpy as np
import matplotlib.pyplot as plt

img_path = "./classification_model/train/4/00008_00046_00028.png"

def image_hist(img, title="Imagem Processada", color = False):
    plt.figure(figsize=(10,4))

    plt.subplot(1,2,1)
    if(color):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.imshow(img_rgb)
    else:
        plt.imshow(img, cmap="gray")
    
    plt.title(title)
    plt.axis("off")

    plt.subplot(1,2,2)
    plt.hist(img.ravel(), bins=256, range=(0,255), color="black")
    plt.title("Histograma")
    plt.xlabel("Intensidade")
    plt.ylabel("Frequência")

    plt.tight_layout()
    plt.show()

def preprocessing(img):
    image_hist(img, "Inicial", color=True)

    # Preto e branco
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    image_hist(img, "Escala de Cinza")

    # Correção gama
    img = np.array(255 * (img / 255) ** 0.8, dtype='uint8')
    image_hist(img, "Gamma 0.8")

    # Redimensionamento
    img = cv2.resize(img, (64, 64), interpolation=cv2.INTER_CUBIC)
    image_hist(img, "Resize 64x64")

    # Equalização adaptativa CLAHE
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    img = clahe.apply(img)
    image_hist(img, "Equalização adaptativa CLAHE")

    # Filtro Gaussiano
    img = cv2.GaussianBlur(img, (3,3), 0)
    image_hist(img, "Filtro Gaussiano")

    # Realce de bordas (Filtro Laplaciano + Sharpening)
    kernel = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])
    sharpened = cv2.filter2D(img, -1, kernel)
    img = cv2.addWeighted(img, 1.0, sharpened, 1.5, 0)
    image_hist(img, "Filtro Laplaciano + Sharpening")

    # Limiarização adaptativa
    img = cv2.adaptiveThreshold(
        img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 15, 7
    )
    image_hist(img, "Limiarização adaptativa")

    # Operações morfológicas
    img = cv2.bitwise_not(img)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=1)  
    img = cv2.erode(img, kernel, iterations=1)  
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=1)
    img = cv2.bitwise_not(img)
    image_hist(img, "Operações morfológicas: Fechamento e Dilatação")

    return img


raw_img = cv2.imread(img_path)
proc_img = preprocessing(raw_img)




