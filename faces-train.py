import os
import cv2 as opencv
from PIL import Image
import pickle
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR,"Images")

face_cascade = opencv.CascadeClassifier("Cascades/data/haarcascade_frontalface_alt2.xml")
recognizer = opencv.face.LBPHFaceRecognizer_create()

current_id = 0
label_ids = {}
x_path = []
y_labels = []

for root, dirs, files in os.walk(IMAGE_DIR):
    for file in files:
        if file.endswith("png") or file.endswith("jpg") or file.endswith("jpeg") or file.endswith("JPG") or file.endswith("JPEG") or file.endswith("PNG"):
            path = os.path.join(root,file)
            label = os.path.basename(os.path.dirname(path)).replace(" ","-").lower()
            #print(label,path)
            
            if not label in label_ids:
                label_ids[label] = current_id
                current_id += 1
                
            id_ = label_ids[label]
            #print(label_ids)
                
            
            pil_image = Image.open(path).convert("L")
            size = (500, 500)
            final_image = pil_image.resize(size, Image.ANTIALIAS)
            image_array = np.array(final_image, "uint8")
            #print(image_array) 
            
            
            faces = face_cascade.detectMultiScale(image_array, scaleFactor = 1.5, minNeighbors=5)
            
            for (x,y,w,h) in faces:
                roi = image_array[y:y+h,x:x+w]
                x_path.append(roi)
                y_labels.append(id_)

with open("labels.pickle",'wb') as f:
    pickle.dump(label_ids,f)
                
recognizer.train(x_path,np.array(y_labels))  
recognizer.save("result.yml")          
            





