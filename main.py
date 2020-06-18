import os
import cv2 as opencv
import numpy as np
import pickle
import PIL
from PIL import Image
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from connect import *

        
def photoRead():
    
    username_get = username_string_signup.get()
    password_get = password_string_signup.get()
    
    if username_get != "" and password_get != "":
        
        filename_pict = filedialog.askopenfilenames(filetypes = (("PNG files","*.png"),("JPEG files","*.jpeg"),("JPG files","*.jpg")))
        
        if filename_pict != None:
            str = ','.join(filename_pict)
            new_str = str.split(",")
            
            
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            IMAGE_DIR = os.path.join(BASE_DIR,"Images")
            
            os.chdir('{}'.format(IMAGE_DIR))
            os.mkdir("{}".format(username_get))
            
            for i in new_str:
                img = PIL.Image.open("{}".format(i))
                head, last = os.path.split(i)
                USER_DIR = '{}\\{}'.format(IMAGE_DIR,username_get)
                os.chdir(USER_DIR)
                img.save("{}".format(last))
        
        
        else:
            messagebox.showerror(title="Error", message="Please Select Photos")
            

        
    else:
        messagebox.showerror(title="Error", message="Username/Password Cannot Be Empty")
        
        
        
def insert_User():
    
    username_db_entry = username_string_signup.get()
    password_db_entry = password_string_signup.get()
    
    sql_command_insert = """ INSERT INTO `face_recognition`(`username`, `password`) VALUES (%s,%s)"""
    sql_columns = (username_db_entry, password_db_entry)
    
    cursor.execute(sql_command_insert, sql_columns)
    
    db_connect.commit()
        
def face_recognizer():
    
    username_get_string = username_string.get()
    
    sql_command =  "SELECT * FROM face_recognition WHERE id"
    cursor.execute(sql_command)
    
    results = cursor.fetchall()
    
    for row in results:
        id_column       = row[0]
        username_column = row[1]
        password_column = row[2]
    
    face_cascade = opencv.CascadeClassifier("Cascades/data/haarcascade_frontalface_alt2.xml")
    recognizer = opencv.face.LBPHFaceRecognizer_create()
    recognizer.read("result.yml")
    
    labels = {"person_name":  1}
    
    with open("labels.pickle","rb") as f:
        
        original_labels = pickle.load(f)
        labels = {v:k for k,v in original_labels.items()}

    cap = opencv.VideoCapture(0)
    
    while(True):

        ret, frame = cap.read()
        greytone = opencv.cvtColor(frame, opencv.COLOR_BGR2GRAY)
        greytone= greytone.astype('uint8')
        faces = face_cascade.detectMultiScale(greytone, scaleFactor = 1.5, minNeighbors=5)
        
        for(x, y, w, h) in faces:
            roi_gray = greytone[y:y+h,x:x+w]
            roi_color = frame[y:y+h,x:x+w]
            
            id_, conf = recognizer.predict(roi_gray)
            
            if conf>=45 and conf<=85:
                if username_get_string == labels[id_] == username_column:
                    font = opencv.FONT_HERSHEY_SIMPLEX
                    name = labels[id_]
                    color = (255, 255, 255)
                    stroke = 2
                    opencv.putText(frame, name, (x,y), font, 1 , color, stroke, opencv.LINE_AA)
                    messagebox.showinfo(title="Success", message="Access Granted")
                    
                
                
            image_item = "8.png"
            opencv.imwrite(image_item,roi_gray)
            
            color = (255, 0, 0)
            stroke = 2
            end_cord_x = x + w
            end_cord_y = y + h
            opencv.rectangle(frame, (x,y), (end_cord_x,end_cord_y), color, stroke)
        
        opencv.imshow("Frame", frame)
        
        if opencv.waitKey(20) & 0xFF == ord("q"):
            break

    cap.release()
    opencv.destroyAllWindows()

def signUP():
    global username_string_signup
    global password_string_signup
    
    top = Toplevel()
    width = 400
    height = 350
    
    screen_width = top.winfo_screenwidth()
    screen_height = top.winfo_screenheight()
    
    x_coordinate = (screen_width/2) - (width/2)
    y_coordinate = (screen_height/2) - (height/2)
    
    top.geometry("%dx%d+%d+%d" % (width,height,x_coordinate,y_coordinate))
    top.title("SIGN UP");

    head_signup = Label(top,text = "SIGN UP", bg = "#003399", fg = "black", width = "250", height = "2")
    head_signup.pack()

    username_string_signup = StringVar()
    password_string_signup = StringVar()

    username_label_signup = Label(top, text = "Kullanıcı Adı")
    username_label_signup.pack(anchor=tk.W,padx=155,pady=10)
    username_textbox_signup = Entry(top,textvariable = username_string_signup, width = "30")
    username_textbox_signup.pack(anchor=tk.W,padx=100,pady=10)
    
    password_label_signup = Label(top, text = "Password")
    password_label_signup.pack(anchor=tk.W,padx=160,pady=10)
    password_textbox_signup = Entry(top, textvariable = password_string_signup, width = "30", show="*")
    password_textbox_signup.pack(anchor=tk.W,padx=100,pady=10)
    

    username_string_get_signup = username_string_signup.get()

    
    signup = Button(top,text = "Sign Up", width = "25", height = "2", command = insert_User, bg = "#006699")
    signup.pack(anchor=tk.W,padx=100,pady=10)
    photoread = Button(top,text = "Photo Read", width = "25", height = "2", command = photoRead, bg = "#006699")
    photoread.pack(anchor=tk.W,padx=100,pady=15)




        
root = tk.Tk()

width = 400
height = 350

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_coordinate = (screen_width/2) - (width/2)
y_coordinate = (screen_height/2) - (height/2)

root.geometry("%dx%d+%d+%d" % (width,height,x_coordinate,y_coordinate))
root.title("SIGN IN");

head = Label(text = "FACE RECOGNITION SYSTEM", bg = "#003399", fg = "black", width = "250", height = "2")
head.pack()

username_string = StringVar()
password_string = StringVar()

username_string_get = username_string.get()

username_label = Label(text = "Username")
username_label.pack(anchor=tk.W,padx=160,pady=10)

username_textbox = Entry(textvariable = username_string, width = "30")
username_textbox.pack(anchor=tk.W,padx=100,pady=10)

password_label = Label(text = "Password")
password_label.pack(anchor=tk.W,padx=160,pady=10)

password_textbox = Entry(textvariable = password_string, width = "30", show="*")
password_textbox.pack(anchor=tk.W,padx=100,pady=10)


register = Button(text = "Sign In", width = "25", height = "2", command = face_recognizer, bg = "#006699")
register.pack(anchor=tk.W,padx=100,pady=10)

signup = Button(text = "Sign Up", width = "25", height = "2", command = signUP, bg = "#006699")
signup.pack(anchor=tk.W,padx=100,pady=15)

root.mainloop()













