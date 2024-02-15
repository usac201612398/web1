'''
import cv2
import numpy as np 
import face_recognition as fr 
import os
import random
from datetime import datetime

class registroFace(os):
    def __init__(img, self):

        self.img = img

    pass

path = 'home/bportillo/Proyecto1/web1/app1/static/app1'
images = []
clases = []
lista = os.listdir(path)
registro = []
comp1 = 100

for i in lista:
    imgdb = cv2.imread(f'{path}/{i}')
    images.append(imgdb)
    clases.append(os.path.splitext(i)[0])

def codRostros(images):
    listaCod = []

    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        cod = fr.face_encodings(img)[0]
        listaCod.append(cod)
    return listaCod
rostrosCod = codRostros(images)
cap = cv2.VideoCapture(0)

while(True):
    ret, frame =cap.read()
    cv2.imshow('Rostro', frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
frame2 = cv2.resize(frame,(0,0),None,0.25,0.25)
rgb = cv2.cvtColor(frame2,cv2.COLOR_BGR2RGB)
faces = fr.face_locations(rgb)
facesCod = fr.face_encodings(rgb,faces)


for facecod, faceloc in zip(facesCod,faces):
    
    comparacion = fr.compare_faces(rostrosCod,facecod)
    simi = fr.face_distance(rostrosCod,facecod)
    min = np.argmin(simi)
    
    if comparacion[min]:
        nombre = clases[min].upper()

        yi, xf, yf, xi = faceloc
        yi, xf, yf, xi = yi*4, xf*4, yf*4, xi*4

        indice = comparacion.index(True)
    
    if comp1!= indice:
        r = random.randrange(0,255,50)
        g = random.randrange(0,255,50)
        b = random.randrange(0,255,50)
        comp1 = indice

    if comp1 == indice:
        cv2.rectangle(frame,(xi,yi),(xf,yf),(r,g,b),3)
        cv2.rectangle(frame,(xi,yf-35),(xf,yf),(r,g,b),cv2.FILLED)
        cv2.putText(frame, nombre,(xi+6,yi-6), cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
        registro.append([nombre,datetime.now()])
        print(registro)

cv2.imshow("Reconocimiento Facial",frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''