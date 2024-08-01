import tkinter as tk
import tkinter.font as font
import cv2
import face_recognition
from PIL import Image, ImageTk
import os
import subprocess
import time

window = tk.Tk()
window.title("Face Recognition")
window.geometry("1024x600+0+0")

canvas = tk.Canvas(window, width=600, height=450)
canvas.pack()

known_face_encodings = []
known_face_names = []
db_path = "db"
for filename in os.listdir(db_path):
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
        image = face_recognition.load_image_file(os.path.join(db_path, filename))
        encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(encoding)
        known_face_names.append(os.path.splitext(filename)[0])

def process_image():
    ret, im = cap2.read()

    rgb_im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_im)
    face_encodings = face_recognition.face_encodings(rgb_im, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.4)

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            
        else:
            name = "Unknown"

        color = (0, 255, 0)
        thickness = 2
        cv2.rectangle(im, (left, top), (right, bottom), color, thickness)

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        color = (255, 255, 255)
        stroke = 2
        cv2.putText(im, name, (left, bottom + 20), font, font_scale, color, stroke, cv2.LINE_AA)

    img = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
    imgtk = ImageTk.PhotoImage(image=img)
    canvas.imgtk = imgtk
    canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)

    window.after(10, process_image)

cap2 = cv2.VideoCapture(0)

process_image()

def gerakmotor() :
    window.destroy()
    cap2.release()
    p = subprocess.run(["python", "stepper_berlawan_jarum_jam.py"])

def open_program():
    window.destroy()
    cap2.release()
    subprocess.run(["python", "Daftar.py"])

open_button = tk.Button(window, text="Daftar", command=open_program,  height= 1, width= 100)
open_button.pack()
my_font = font.Font(size=80)
open_button.configure(font=my_font)

window.mainloop()
