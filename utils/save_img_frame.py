import cv2
import numpy as np
from keras.models import  load_model

video = cv2.VideoCapture(1,cv2.CAP_DSHOW)
file_qtde = 0
coin_num = 25

def pre_process(img):
    kernel = np.ones((4, 4), np.uint8)

    img_pro = cv2.GaussianBlur(img,(5,5),3)
    img_pro = cv2.Canny(img_pro,90,140)
    img_pro = cv2.dilate(img_pro, kernel, iterations=2)
    img_pro = cv2.erode(img_pro, kernel, iterations=1)

    return img_pro

while True:
    _,img = video.read()
    img = cv2.resize(img, (640, 480))
    img_pro = pre_process(img)
    countors,hi = cv2.findContours(img_pro, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    for cnt in countors:
        area = cv2.contourArea(cnt)

        if area > 2000:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(img,(x,y), (x + w, y + h), (0, 0, 0), 2)
            
            coin_frame = img[y:y + h, x:x + w]

            key = cv2.waitKey(1) & 0xFF  # Espera por uma tecla

            if key == ord('s'):  # Se a tecla 's' for pressionada
                cv2.imwrite(f'../images/samples/{coin_num}/n-{file_qtde}.jpg', coin_frame)
                print(f'Saved')
                file_qtde += 1

    cv2.imshow('IMG', img)
    cv2.waitKey(1)