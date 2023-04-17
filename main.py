import cv2
import numpy as np
from keras.models import  load_model

video = cv2.VideoCapture(1,cv2.CAP_DSHOW)

model = load_model('Keras_model.h5',compile=False)
data = np.ndarray(shape=(1,224,224,3),dtype=np.float32)
classes = [25, 50]

def pre_process(img):
    kernel = np.ones((4, 4), np.uint8)

    img_pro = cv2.GaussianBlur(img,(5,5),3)
    img_pro = cv2.Canny(img_pro,90,140)
    img_pro = cv2.dilate(img_pro, kernel, iterations=2)
    img_pro = cv2.erode(img_pro, kernel, iterations=1)

    return img_pro

def detect_coin(img):
    coin_img = cv2.resize(img,(224,224))
    coin_img = np.asarray(coin_img)
    normalize_img = (coin_img.astype(np.float32) / 127.0) - 1
    data[0] = normalize_img
    prediction = model.predict(data)
    index = np.argmax(prediction)
    confidence_score = prediction[0][index]
    class_name = classes[index]
    return  class_name, confidence_score

while True:
    _,img = video.read()
    img = cv2.resize(img, (640, 480))
    img_pro = pre_process(img)
    countors,hi = cv2.findContours(img_pro, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    count_value = 0
    for cnt in countors:
        area = cv2.contourArea(cnt)
        if area > 2000:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(img,(x,y), (x + w, y + h), (0, 255, 0), 2)
            coin_frame = img[y:y + h, x:x + w]

            class_name, confidence_score = detect_coin(coin_frame)

            if confidence_score > 0.7:
                cv2.putText(img, str(class_name), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),2)

                if class_name == 25: count_value += 0.25
                if class_name == 50: count_value += 0.5

    cv2.rectangle(img, (430, 30), (600, 80), (0, 0, 255), -1)
    cv2.putText(img,f'R$ {count_value}',(440,67),cv2.FONT_HERSHEY_SIMPLEX,1.2,(255,255,255),2)

    cv2.imshow('IMG', img)
    cv2.imshow('IMG PROCESSED', img_pro)
    cv2.waitKey(1)