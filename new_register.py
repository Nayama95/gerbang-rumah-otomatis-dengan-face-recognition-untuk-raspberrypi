import os.path
import subprocess
import tkinter as tk
import cv2
import util
from PIL import Image, ImageTk
import datetime

class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.title("Face Recognition")
        self.main_window.geometry("1024x600+0+0")

        self.register_new_user_button_main_window = util.get_button(self.main_window, 'register new user',
                                                                    'green', self.register_new_user,
                                                                    fg='black')
        self.register_new_user_button_main_window.place(x=700, y=250)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, height=500)

        self.add_webcam(self.webcam_label)
        
        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)
    
    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap= cv2.VideoCapture(0)

        self._label= label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()
        self.most_recent_capture_arr= frame

        img = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_pil=Image.fromarray(img)

        imgtK= ImageTk.PhotoImage(image=self.most_recent_pil)
        self._label.imgTk= imgtK
        self._label.configure(image=imgtK)

        self._label.after(20, self.process_webcam)
    
    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1024x600+0+0")

        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept',
                                                                       'green',self.accept_button_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=300)

        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window,
                                                                         'Try Again', 'red',
                                                                         self.try_again_button_register_new_user)
        self.try_again_button_register_new_user_window.place(x=750, y=400)

        self.entry_text_regsiter_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_regsiter_new_user.place(x=750, y=150)

        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, 'Masukan Nama '
                                                                                               ' \nAwalan Huruf Kapital:')
        self.text_label_register_new_user.place(x=750, y=70)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.add_image_to_label(self.capture_label)

    def add_image_to_label(self, label):
        imgtK = ImageTk.PhotoImage(image=self.most_recent_pil)
        label.imgTk = imgtK
        label.configure(image=imgtK)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def accept_button_register_new_user(self):
        name = self.entry_text_regsiter_new_user.get(1.0, "end-1c")

        cv2.imwrite(os.path.join(self.db_dir, '{}.png'.format(name)),self.register_new_user_capture)

        util.msg_box('Sucess','Berhasil')

        self.register_new_user_window.destroy()
        self.main_window.destroy()
        self.cap.release()
        subprocess.run(["python", "Daftar.py"])

    def try_again_button_register_new_user(self):
       self.register_new_user_window.destroy()

    def start(self):
         self.main_window.mainloop()

if __name__ == "__main__":
    app = App()
    app.start()