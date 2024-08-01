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

        self.login_button_main_window = util.get_button(self.main_window, 'login', 'green',self.login)
        self.login_button_main_window.place(x=700, y=10)
        self.register_new_user_button_main_window = util.get_button(self.main_window, 'Real Time', 'red',
                                                                    self.realtime, fg='black')
        self.register_new_user_button_main_window.place(x=700, y=100)
        self.register_new_user_button_main_window = util.get_button(self.main_window, 'Delete File', 'blue',
                                                                    self.delete_file, fg='black')
        self.register_new_user_button_main_window.place(x=700, y=190)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = './log.txt'

    def delete_file(self):
        self.main_window.destroy()
        self.cap.release()
        subprocess.run(["python", "Delete.py"])

    def realtime (self):
        self.main_window.destroy()
        self.cap.release()
        subprocess.run(["python", "realtime.py"])

    def refresh(self):
        self.main_window.destroy()
        self.__init__()

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
    def login(self):
        unknown_img_path = './siapa/tmp.png'
        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)
        output = str(subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]))
        name = output.split(',')[1][:-5]
        if name in ['unknown_person', 'no_persons_found']:
            util.msg_box('Waduh', 'siapa kamu')
        else:
            util.msg_box('selamat datang', 'hallo, {}'.format(name))
            self.main_window.destroy()
            self.cap.release()
            subprocess.run(["python", "new_register.py"])
            with open(self.log_path, 'a') as f:
                f.write('{},{}\n'.format(name, datetime.datetime.now()))
                f.close()

        os.remove(unknown_img_path)

    def start(self):
         self.main_window.mainloop()

if __name__ == "__main__":
    app = App()
    app.start()
