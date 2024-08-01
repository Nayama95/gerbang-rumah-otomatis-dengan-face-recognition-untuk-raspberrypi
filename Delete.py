import os
import tkinter as tk
import subprocess
import util

def delete_file():
    filename = text_box.get("1.0", "end-1c")
    folder_path = "db"
    try:
        for file in os.listdir(folder_path):
            if file.endswith(".png") and file.startswith(filename):
                os.remove(os.path.join(folder_path, file))
                util.msg_box("Berhasil", "File {} berhasil dihapus".format(filename))
    except Exception :
        util.msg_box("File {} tidak ditemukan".format(filename))

def tampilkan_file():
    path = "db"
    for widget in frame.winfo_children():
        widget.destroy()
    for i, file in enumerate(os.listdir(path)):
        label = tk.Label(frame, text=file)
        label.grid(row=i, column=0)

def open_program():
    window.destroy()
    subprocess.run(["python", "Daftar.py"])

window = tk.Tk()
window.title("Face Recognition")
window.geometry("1024x600+0+0")

text_box = util.get_entry_text(window)
text_box.place(x=7, y=5)

delete_button = util.get_button(window, 'Delete', 'green',delete_file)
delete_button.place(x=7, y=110)

daftar_button = util.get_button(window, 'Daftar', 'Red',open_program)
daftar_button.place(x=7, y=200)

file_button = util.get_button(window, 'File', 'Blue',tampilkan_file)
file_button.place(x=7, y=290)

frame = tk.Frame(window)
frame.pack()

window.mainloop()

