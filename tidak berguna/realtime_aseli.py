import tkinter as tk
import tkinter.font as font
import cv2
import face_recognition
from PIL import Image, ImageTk
import os
import subprocess

# Create GUI
window = tk.Tk()
window.title("Face Recognition")
window.geometry("1024x600+0+0")

# Create a canvas to display the image
canvas = tk.Canvas(window, width=600, height=450)
canvas.pack()

# Load the known faces and their names
known_face_encodings = []
known_face_names = []
db_path = "db"
for filename in os.listdir(db_path):
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
        image = face_recognition.load_image_file(os.path.join(db_path, filename))
        encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(encoding)
        known_face_names.append(os.path.splitext(filename)[0])

# Process the image
def process_image():
    # Capture a im from the video feed
    ret, im = cap2.read()

    # Convert the im to RGB
    rgb_im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

    # Find all the faces in the im
    face_locations = face_recognition.face_locations(rgb_im)
    face_encodings = face_recognition.face_encodings(rgb_im, face_locations)

    # Process each face in the im
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for any of the known faces
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        # If there's a match, display the name of the person
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
        else:
            name = "Unknown"

        # Draw a rectangle around the face
        color = (0, 255, 0)
        thickness = 2
        cv2.rectangle(im, (left, top), (right, bottom), color, thickness)

        # Display the name of the person
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        color = (255, 255, 255)
        stroke = 2
        cv2.putText(im, name, (left, bottom + 20), font, font_scale, color, stroke, cv2.LINE_AA)

    # Convert the im to an ImageTk object and display it on the canvas
    img = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
    imgtk = ImageTk.PhotoImage(image=img)
    canvas.imgtk = imgtk
    canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)

    # Schedule the next call to process_image
    window.after(10, process_image)

# Capture video from the default camera
cap2 = cv2.VideoCapture(0)

# Start processing the image
process_image()

# Add button to open another program
def open_program():
    window.destroy()
    cap2.release()
    subprocess.run(["python", "Daftar.py"])

open_button = tk.Button(window, text="Daftar", command=open_program,  height= 1, width= 100)
open_button.pack()
my_font = font.Font(size=80)
open_button.configure(font=my_font)

# Start the GUI event loop
window.mainloop()
